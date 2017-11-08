export default [ '$scope','$http', function ($scope,$http) {

    $scope.user_message = ''
    $scope.message_history = []

    $scope.message = () => {
        
        let user_message = {
            source:'user',
            date: Date.now(),
            message: $scope.user_message
        }
        
        $scope.message_history.unshift(user_message)
        
        $http({
            url: '/chatbot/v1.1/message/',
            method: "POST",
            data: `message=${$scope.user_message}`,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
        }).then(
            res=>{
                let bot_message = {
                    source : 'bot',
                    date: Date.now(),
                    message: res.data.message
                }
                
                $scope.message_history.unshift(bot_message)
                // $scope.json_message = res.data.nlu
                $scope.nlu_last_response = JSON.stringify(res.data, undefined, 2);
                $scope.user_message = ''
            }
        )
        
    }
    
}]