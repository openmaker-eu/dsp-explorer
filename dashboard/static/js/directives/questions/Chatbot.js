let _ = require('lodash')
let $ = require('jquery')

let template = `
    <div class="chatbot" ng-if="$root.authorization > 0">
        <div class="chatbot__container">
            <div class="chatbot__header" style="width: 100%; height:50px; background: #f00;"></div>
            <div class="chatbot__body" ng-if="opened" style="background: white;">
                <wizard
                    questions="questions"
                    action="chatbot"
                    loadingmessage="Chatbot is writing"
                    wizardid="wizardid"
                ></wizard>
                <navi-chatbot items="questions" wizardid="wizardid"></navi-chatbot>
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
        $scope.wizardid = $scope.$id
        
        $scope.toggle_bot = ()=>($scope.opened=!$scope.opened)
    
        $scope.welcome_question = {
            name:'welcome',
            type: "question",
            question: 'Hi, '+_.get($rootScope, 'user.first_name')+'!',
            text: "Do you have time for some questions?",
            actions:{options:[{label:'yes, sure!'},  {value:'goto:last', label:'no, thanks'}]}
        }
        $scope.end_question = {type: "question", question: "Nice talking "+_.get($rootScope, 'user.first_name')+"!", text:"Have a nice day", actions:{options:['  Bye!  ']}}
    
        $scope.get = ()=> {
            $scope.opened = false
            $http
                .get($scope.url())
                .then($scope.handle_response)
                .catch((e) => {console.log(e)})
        }
        
        $scope.url = ()=>{
            let page_options = _.get($rootScope, 'page_info.options')
            let url = '/api/v1.4/questions/chatbot/'
            page_options.hasOwnProperty('entity_name') && (url += '?entity_name='+page_options['entity_name'])
            page_options.hasOwnProperty('entity_id') && (url += '&entity_id='+page_options['entity_id'])
            return url
        }
        
        $scope.handle_response = (res)=>{
            if(_.isArray(res.data.questions) && res.data.questions.length > 0) {
                $scope.questions =  _($scope.welcome_question).concat(res.data.questions).concat($scope.end_question).value()
                $timeout(function(a){ $scope.opened = true }, 5000)
            }
            
        }
    
        $rootScope.$on('wizard.'+$scope.wizardid+'.end', ()=>{ console.log('CHAtbot END', $scope.$id); $scope.opened=false })
        $rootScope.$on('authorization.refresh', $scope.get())
    
    }]
}

export default [()=>chatbot_directive]

