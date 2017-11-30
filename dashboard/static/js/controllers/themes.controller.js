import * as _ from 'lodash'

export default [ '$scope','$uibModal','$http','$aside', function ($scope,$uibModal,$http,$aside) {
    
    let feed = {
        theme : null,
        filter : 'yesterday' ,
        current_cursor : null,
        next_cursor : 0,
        progress : false,
        top:  $(window).scrollTop(),
        data : [],
        
        prev : function(){$scope.FeedModel.get_news()},
        next : function(){$scope.FeedModel.get_news()},
        
        reset : function(theme=feed.theme, filter=feed.filter, cursor=-1){
            feed.data = []
            feed.current_cursor = null
            feed.next_cursor = 0,
            feed.next(theme, filter, cursor)
            return feed
        },
        
        get_news : function(theme=feed.theme , filter=feed.filter , cursor = feed.next_cursor){
            $http.get('/api/v1.3/news/' + (theme || 1) + '/' + filter + '/' + cursor + '/')
                .then(
                    (response) => {
                        feed.data = _.get(response, 'data.result.news')
                        feed.next_cursor = _.get(response, 'data.result.next_cursor')
                        
                        console.log(response);
                        console.log(feed.data);
                        console.log(feed.next_cursor);
                    },
                    (err)=>{ console.log('ERROR:', err)}
                )
            return feed
        }
    }
    
    
    let influencers = {
        influencers : [],
        audiences : [],
        get_influencers : function (theme) {
            $http.get('/api/v1.3/influencers/' + (theme || 1) + '/')
                .then(
                    function (response) {influencers.influencers = _.get(response, 'data.result.local_influencers')},
                    function (err) { /* ToDo show API errors with a common error message using toastr? */}
                )
        },
        get_audiences : function (theme) {
            $http.get('/api/v1.3/audiences/' + (theme || 1) + '/' )
                .then(
                    function (response) {influencers.audiences = _.get(response, 'data.result.audience_sample')},
                    function (err) { /* ToDo show API errors with a common error message using toastr? */}
                )
        }
    }
    
    $scope.FeedModel = feed
    $scope.InfluencersModel = influencers
    
    let unbind_topic_id = $scope.$watch('topic_id', function (newValue, oldValue) {
        // if(newValue === oldValue) return
        $scope.FeedModel.theme = newValue
        $scope.FeedModel.get_news(newValue, $scope.filter, $scope.cursor)
        influencers.get_audiences($scope.topic_id);
        influencers.get_influencers($scope.topic_id);
        unbind_topic_id()
    })
    
    // Set filter for time
    $scope.setFilter = function (filter) {
        if($scope.FeedModel.progress==false){
            $scope.FeedModel.filter = filter;
            $scope.FeedModel.reset($scope.theme)
        }
    }
    
    //
    // let audiences_watch = $scope.$watch('topic_id', ()=>{  audiences_watch=null})
    // let influencers_watch = $scope.$watch('topic_id', ()=>{ influencers.get_influencers($scope.topic_id); influencers_watch=null})

    
}]