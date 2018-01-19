/**
 * Created by andreafspeziale on 06/07/17.
 */

export default [ '$scope', '$http', '$sce', function ($scope, $http, $sce) {

    $scope.show_canvas = true
    $scope.no_data_message = ''

    $scope.canvas_info = {
        base_url: '',
        user_profile_twitter_username: '',
        url: ''
    }

    $scope.checkCanvasData = (canvas_url, username) => {
        $http.get('api/v1.2/check_canvas/' + username).then(
            function(response) {
                $scope.show_canvas = response.data.result
                if ( !response.data.result ) $scope.no_data_message = 'No data'
                $scope.canvas_info.user_profile_twitter_username = username
                $scope.canvas_info.url = $sce.trustAsResourceUrl(canvas_url+username)
            }, function(err) {
                console.log("error")
                console.log(err)
                $scope.show_canvas = false
            });
    }

    $scope.updateUsername = (username) => {
        if(username!='') {
            $scope.canvas_info.user_profile_twitter_username = username
            $scope.no_data_message = ''
        }
    }

    $scope.$watch('[canvas_info.base_url,canvas_info.user_profile_twitter_username]', function (newValue, oldValue) {
        $scope.checkCanvasData(newValue[0], newValue[1])
    })

}]