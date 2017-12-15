import * as _ from 'lodash'

export default [ '$scope','$uibModal','$http','$aside', function ($scope,$uibModal,$http,$aside) {
    
    $scope.selected_location = ''
    
    let feed = {
        theme : null,
        filter : 'yesterday' ,
        next_cursor : 0,
        prev_cursor : undefined,
        
        progress : false,
        top:  $(window).scrollTop(),
        data : [],
    
        prev : function(){$scope.FeedModel.get_news(feed.prev_cursor)},
        next : function(){$scope.FeedModel.get_news(feed.next_cursor)},
        
        reset : function(theme=feed.theme, filter=feed.filter, cursor=-1){
            feed.data = []
            feed.next_cursor = 0,
            feed.next(theme, filter, cursor)
            return feed
        },
        
        get_news : function(cursor = -1 , theme=feed.theme , filter=feed.filter){
            $http.get('/api/v1.3/news/' + (theme || 1) + '/' + filter + '/' + cursor + '/')
                .then(
                    (response) => {
                        feed.data = _.get(response, 'data.result.news')
                        feed.next_cursor = _.get(response, 'data.result.next_cursor')
                        feed.prev_cursor = _.get(response, 'data.result.prev_cursor')
                    },
                    (err)=>{ console.log('ERROR:', err)}
                )
            return feed
        }
    }
    
    
    let influencers = {
        theme: null,
        location:null,
        influencers : [],
        audiences : [],
        get_influencers : function (theme) {
            $http.get('/api/v1.3/influencers/' + (theme || influencers.theme || 1) + '/' +(influencers.location || ''))
                .then(
                    function (response) {influencers.influencers = _.get(response, 'data.result.local_influencers')},
                    function (err) { /* ToDo show API errors with a common error message using toastr? */}
                )
        },
        get_audiences : function (theme) {
            $http.get('/api/v1.3/audiences/' + (theme || influencers.theme || 1) + '/' +(influencers.location || ''))
                .then(
                    function (response) {influencers.audiences = _.get(response, 'data.result.audience_sample')},
                    function (err) { /* ToDo show API errors with a common error message using toastr? */}
                )
        },
        get_all : function(){
            influencers.get_audiences()
            influencers.get_influencers()
        },
        set_location : function(location){ influencers.location = location, influencers.get_all() }
    }
    
    $scope.FeedModel = feed
    $scope.InfluencersModel = influencers
    
    let unbind_topic_id = $scope.$watch('topic_id', function (newValue, oldValue) {
        
        // Set Theme for this page
        $scope.FeedModel.theme = newValue
        influencers.theme = newValue
        influencers.location = $scope.selected_location
        
        // Get all data
        $scope.FeedModel.get_news(newValue, $scope.filter, $scope.cursor)
        influencers.get_audiences($scope.topic_id);
        influencers.get_influencers($scope.topic_id);
        
        console.log(influencers.location);
        
        // Unbind to execute watch only once
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