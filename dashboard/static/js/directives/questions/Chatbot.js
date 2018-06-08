let _ = require('lodash')
let $ = require('jquery')

let template = `
    <div class="chatbot">
        <div class="chatbot__container">
            <div class="chatbot__header" style="width: 100%; height:50px; background: #f00;"></div>
            <div class="chatbot__body" style="background: white;">
                <wizard questions="questions" action="acttion" loadingmessage="Chatbot is writing"></wizard>
            </div>
        </div>
    </div>
`

let chatbot_directive =
{
    template:template,
    scope: {},
    controller: ['$scope', '$rootScope', '$http', function($scope, $rootScope, $http){
        $('chatbot').css('bottom', $('footer').height()+'px')
        
        $scope.questions= null
        $scope.action= 'chatbot.question.simple'
        
        
        $http
            .get('/api/v1.4/questions?action=chatbot.question')
            .then(res=>$scope.questions=res.data.questions)
            .catch((e)=>{console.log(e);})
        
    }]
}

export default [()=>chatbot_directive]

