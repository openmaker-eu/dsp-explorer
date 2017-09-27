/**
 * Created by andreafspeziale on 24/05/17.
 */
export default [ '$scope','$uibModal','$http','$aside', function ($scope,$uibModal,$http,$aside) {

    $scope.filter = 'yesterday'
    $scope.cursor = -1
    
    $scope.FeedModel = {
        theme : null,
        filter : 'yesterday' ,
        current_cursor : null,
        next_cursor : -1,
        progress : false,
        top:  $(window).scrollTop(),
        data : [],
        
        next : function( theme = this.theme , filter = this.filter , cursor = this.next_cursor){
            if(
                this.progress === true
                || this.next_cursor == 0
                || this.current_cursor == this.next_cursor
            ) return
            
            this.progress = true;
            this.current_cursor = this.next_cursor
            this.get_news( theme, filter, cursor )
            return this
            
        },
        
        get : function(theme=this.theme, filter=this.filter, cursor=this.next_cursor){
            this.data = []
            this.current_cursor = null
            this.next_cursor = -1
            this.next(theme, filter, cursor)
            return this
        },
        
        get_news : function(theme=this.theme , filter=this.filter , cursor = this.next_cursor){
            $http.get('/api/v1.2/news/' + theme + '/' + filter + '/' + cursor + '/')
                .then(
                    (response) => {
                        this.data = this.data.concat(response.data.result.news)
                        this.next_cursor = parseInt(response.data.result.next_cursor)
                        this.progress = false;
                    },
                    this.error
                )
            return this
        },
        get_audiences : function (theme) {
            $http.get('/api/v1.2/audiences/' + theme)
                .then(function (response) {
                    $scope.influencers = response.data.result.audiences;
                },function (err) {
                    // ToDo show API errors with a common error message using toastr?
                })
        }
    }
    
    $scope.$watch('topic_id', function (newValue, oldValue) {
        // if(newValue === oldValue) return
        $scope.FeedModel.theme = newValue
        $scope.FeedModel.get_news(newValue, $scope.filter, $scope.cursor)
        // $scope.FeedModel.next();
        $scope.FeedModel.get_audiences(newValue)
    })
    
    // ToDo make yesterday filter active as default [css] and change active class when other filters are selected
    $scope.setFilter = function (filter) {
        $scope.filter = filter;
        $scope.FeedModel.filter = filter;
    }

    // fired when time filter is changed
    $scope.$watch('filter', function (newValue, oldValue) {
        // get feeds with new filter
        if(newValue != oldValue) $scope.FeedModel.get($scope.theme, newValue, $scope.cursor)
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