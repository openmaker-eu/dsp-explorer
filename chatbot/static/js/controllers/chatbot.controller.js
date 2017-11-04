export default [ '$scope','$http', function ($scope,$http) {

    $scope.user_message = ''

    $scope.message_history = []

    $scope.message = () => {

        $http({
            url: '/chatbot/v1.1/message/',
            method: "POST",
            data: `message=${$scope.user_message}`,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
        }).then(
            res=>{
                $scope.message_history.unshift(res.data)
                // $scope.json_message = res.data.nlu
                $scope.message_history_nlu = JSON.stringify($scope.message_history[0].nlu, undefined, 2);
            }
        )
        
    }
    
}]