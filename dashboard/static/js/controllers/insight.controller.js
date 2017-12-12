/**
 * Created by andreafspeziale on 06/07/17.
 */

export default [ '$scope', '$http', '$sce', function ($scope, $http, $sce) {

    $scope.canvas_info = {
        base_url: '',
        user_profile_twitter_username: '',
        url: ''
    }

    $scope.update_username = (username) => {
        console.log(username)
        if(username!='')
            $scope.canvas_info.user_profile_twitter_username = username
    }

    $scope.$watch('[canvas_info.base_url,canvas_info.user_profile_twitter_username]', function (newValue, oldValue) {
        // update if new value different from old
        $scope.canvas_info.url = $sce.trustAsResourceUrl(newValue[0] + newValue[1])
    })

}]