/**
 * Created by andreafspeziale on 24/05/17.
 */
export default [ '$scope','$uibModal','$http','$aside', function ($scope,$uibModal,$http,$aside) {

    $scope.filter = 'yesterday'
    $scope.cursor = -1
    
    $scope.FeedModel = (()=>{
    
        let get_feed = (theme , filter , cursor = -1 ) => $http.get('/api/v1.1/get_feeds/' + theme + '/' + filter + '/' + cursor)
        
        let model = {
            
            theme : null,
            filter : 'yesterday' ,
            current_cursor : null,
            next_cursor : -1,
            progress : false,
            top:  $(window).scrollTop(),
            
            data : [],
            
            next : ( theme = model.theme , filter = model.filter , cursor = model.next_cursor) => {
                
                if(
                    model.progress === true
                    || model.next_cursor == 0
                    || model.current_cursor == model.next_cursor
                ) return
                
                model.progress = true;
                model.current_cursor = model.next_cursor
                
                return get_feed( theme, filter, cursor )
                    .then(
                        (response) => {
                            model.data = model.data.concat( response.data.result.feeds )
                            model.next_cursor = parseInt( response.data.result.next_cursor )
                            model.progress = false;
                        },
                        model.error
                    )
            
            },
            
            get : ( theme = model.theme , filter = model.filter , cursor = model.next_cursor) => {
    
                console.log('get');
                model.data = []
                model.current_cursor = null
                model.next_cursor = -1
                
                return model.next(theme, filter, cursor)
                
            }
            
        }
        
        return model
        
    }) ()
    
    $(window).scroll(function() {
        console.log( $(window).scrollTop() );
        console.log('top', $('.infinite-container').offset() )
        
    });
    
    
    // ToDo make yesterday filter active as default [css] and change active class when other filters are selected
    $scope.setFilter = function (filter) {
        $scope.filter = filter;
        $scope.FeedModel.filter = filter;
    }
    

    // get feed by theme filter cursor
    // ToDo move API call to explorer factory
    let getFeed = function (theme, filter, cursor) {
        $http.get('/api/v1.1/get_feeds/' + theme + '/' + filter + '/' + cursor)
            .then(function (response) {
                $scope.feeds = response.data.result.feeds
                $scope.cursor = response.data.result.next_cursor;
            },function (err) {
                // ToDo show API errors with a common error message using toastr?
                console.log(err)
            })
    }

    // get influencers by theme
    let getInfluencers = function (theme) {
        $http.get('/api/v1.1/get_influencers/' + theme)
            .then(function (response) {
                $scope.influencers = response.data.result.influencers;
            },function (err) {
                // ToDo show API errors with a common error message using toastr?
                console.log(err)
            })
    }

    // fired when django theme var in loaded in angular
    $scope.$watch('dj', function (newValue, oldValue) {
        $scope.theme = newValue.theme
        console.log($scope.FeedModel, newValue, oldValue );
        
        // $scope.theme = newValue.theme
        $scope.FeedModel.theme = newValue.theme
        
        // get feeds
        // getFeed($scope.theme, $scope.filter, $scope.cursor)
        $scope.FeedModel.next().then(()=>{console.log($scope.FeedModel, newValue, oldValue );})
        
        // get influencers
        getInfluencers($scope.theme)
        
    })

    // fired when time filter is changed
    $scope.$watch('filter', function (newValue, oldValue) {
        // get feeds with new filter
        if(newValue != oldValue) $scope.FeedModel.get($scope.theme, newValue, $scope.cursor)
    
        // getFeed($scope.theme, newValue, $scope.cursor)
    })

    // open aside with influencers
    // ToDo template style
    $scope.openAside = () => {
        $scope.aside = $aside({
            scope:$scope,
            title: "Title",
            templateUrl: false,
            backdrop: 'static',
            template: require("../../../templates/aside/influencers.html"),
            show:false
        });
        $scope.aside.$promise.then(function() {
            $scope.aside.show();
            $('body').addClass('no-scroll');
        })
    }
    $scope.closeAside = () =>{
        $scope.aside.hide()
        $('body').removeClass('no-scroll');
        
    }
    
}]