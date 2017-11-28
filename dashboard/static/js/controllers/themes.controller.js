/**
 * Created by andreafspeziale on 24/05/17.
 */
export default [ '$scope','$uibModal','$http','$aside', function ($scope,$uibModal,$http,$aside) {
    
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
    
        reset : function(theme=this.theme, filter=this.filter, cursor=-1){
            this.data = []
            this.current_cursor = null
            this.next_cursor = -1
            this.next(theme, filter, cursor)
            return this
        },
        
        get_news : function(theme=this.theme , filter=this.filter , cursor = this.next_cursor){
            console.log('get news');
            this.progress = true;
            $http.get('/api/v1.2/news/' + theme + '/' + filter + '/' + cursor + '/')
                .then(
                    (response) => {
                        console.log('get news response');
                        this.data = this.data.concat(response.data.result.news)
                        this.next_cursor = parseInt(response.data.result.next_cursor)
                        this.progress = false;
                    },
                    (err)=>{ console.log('ERROR:', err); this.progress = false; }
                )
            return this
        },
        get_influencers : function (theme) {
            $http.get('/api/v1.3/influencers/' + theme)
                .then(function (response) {
                    $scope.influencers = response.data.result.audiences;
                },function (err) {
                    // ToDo show API errors with a common error message using toastr?
                })
        },
        get_audiences : function (theme) {
            $http.get('/api/v1.3/audiences/' + theme)
                .then(function (response) {
                    $scope.audiences = response.data.result.audiences;
                },function (err) {
                    // ToDo show API errors with a common error message using toastr?
                })
        }
    }
    
    let unbind_topic_id = $scope.$watch('topic_id', function (newValue, oldValue) {
        console.log('default topic');
        // if(newValue === oldValue) return
        $scope.FeedModel.theme = newValue
        $scope.FeedModel
            .get_news(newValue, $scope.filter, $scope.cursor)
            .get_audiences(newValue)
        unbind_topic_id()
    })
    
    // Set filter for time
    $scope.setFilter = function (filter) {
        console.log('Set filter');
        if($scope.FeedModel.progress==false){
            console.log('SET filter inside');
            $scope.FeedModel.filter = filter;
            $scope.FeedModel.reset($scope.theme)
        }
    }

    // open aside with influencers
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