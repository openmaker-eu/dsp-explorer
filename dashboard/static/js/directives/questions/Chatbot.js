let _ = require('lodash')
let $ = require('jquery')

let template = `
    <div class="chatbot">
        <div class="chatbot__container">
            <div class="chatbot__header" >
                <h2>
                    <div class="entity-actions" ng-if="entityname && entityid">
                        <bookmark-button entityname="{$ entityname $}" entityid="{$ entityid $}"></bookmark-button>
                        <interest-button entityname="{$ entityname $}" entityid="{$ entityid $}"></interest-button>
                    </div>
                    
                    <div class="chatbot__toggler pointer">
                        <span
                            class="fas fa-chevron-up text-white"
                            ng-class="{'fa-chevron-down':opened, 'fa-chevron-up':!opened}"
                            ng-click="toggle_bot()"
                        ></span>
                    </div>

                </h2>
                
            </div>
            <div class="chatbot__body" ng-if="opened" style="background: white;">
                <wizard
                    questions="questions"
                    action="chatbot"
                    loadingmessage="I'm writing"
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
    controller: ['$scope', '$rootScope', '$http', '$timeout', 'EntityProvider', function($scope, $rootScope, $http, $timeout, EntityProvider){
        //$('chatbot').css('bottom', $('footer').height()+'px')
        
        $scope.questions= null
        $scope.opened= true
        $scope.wizardid = $scope.$id
        
        $scope.toggle_bot = ()=>($scope.opened=!$scope.opened)
    
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
            if(page_options.hasOwnProperty('entity_name')){
                url += '?entity_name='+page_options['entity_name']
                page_options.hasOwnProperty('entity_id') && (url += '&entity_id='+page_options['entity_id'])
                page_options.hasOwnProperty('entity_temp_id') && (url += '&entity_temp_id='+page_options['entity_temp_id'])
            }
            return url
        }
        
        $scope.handle_response = (res)=>{
            if(_.isArray(res.data.questions) && res.data.questions.length > 0) {
                $scope.questions = res.data.questions
                $timeout(function(a){ $scope.opened = true }, 5000)
            }
            
        }
    
        $rootScope.$on('wizard.'+$scope.wizardid+'.end', ()=>{ $scope.opened=false })
        $rootScope.$on('authorization.refresh', $scope.get())
    
        $scope.entityname = _.get($rootScope, 'page_info.options.entity_name')
        $scope.entityid = _.get($rootScope, 'page_info.options.entity_id')
    
    }]
}

export default [()=>chatbot_directive]

