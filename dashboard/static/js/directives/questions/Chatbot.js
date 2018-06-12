let _ = require('lodash')
let $ = require('jquery')

let template = `
    <div class="chatbot" >
        <div class="chatbot__container">
            <div class="chatbot__header" style="width: 100%; height:50px; background: #f00;"></div>
            <div class="chatbot__body" ng-if="opened" style="background: white; transition: all 2s ease-out;">
                <wizard ng-if="show"
                    questions="questions"
                    action="chatbot"
                    loadingmessage="Chatbot is writing"
                    onend="chatbot.close"
                ></wizard>
            </div>
        </div>
    </div>
`

let chatbot_directive =
{
    template:template,
    scope: {},
    controller: ['$scope', '$rootScope', '$http', '$timeout', function($scope, $rootScope, $http, $timeout){
        $('chatbot').css('bottom', $('footer').height()+'px')
        
        $scope.questions= null
        $scope.opened= true
        $scope.show = true
        
        $scope.toggle_bot = ()=>($scope.opened=!$scope.opened)
    
        $scope.get = ()=> {
            $scope.show = false
            $http
                .get('/api/v1.4/questions/chatbot')
                .then(res => {$scope.questions = res.data.questions})
                .catch((e) => {console.log(e)})
                .finally(() => {$timeout(function(a){ $scope.show = true }, 1000) })
        }
        $scope.get()
    
        $rootScope.$on('chatbot.close', ()=>$scope.opened=false)
        $rootScope.$on('authorization.refresh', ()=>{ console.log('## Refresh'); $scope.get() })
    
    }]
}

export default [()=>chatbot_directive]

