let _ = require('lodash')
let $ = require('jquery')

let template = `
    <div class="chatbot">
        <div class="chatbot__container">
            
            <div class="chatbot__header mobile__padding" >
                <h2 class="chatbot__header__flex">
                    <div class="entity-actions" >
                        <interest-button entityname="news" entityid="{$ entityid $}" isstatic="true"></interest-button>
                        <interest-button entityname="{$ entityname == 'challenges' ? 'challenges' : 'projects' $}"
                            entityid="{$ entityid $}" isstatic="true"
                        ></interest-button>
                        <interest-button entityname="events" entityid="{$ entityid $}" isstatic="true"></interest-button>

                    </div>
                    
                    <div class="chatbot__toggler pointer">
                        <span
                            class="fas fa-chevron-up text-white"
                            ng-class="{'fa-chevron-down':opened && !force_close, 'fa-chevron-up':!opened || force_close}"
                            ng-click="toggle_bot()"
                        ></span>
                    </div>
                </h2>
               
            </div>
            <div class="chatbot__body" ng-if="opened && !force_close" style="background: white;">
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
        
        $scope.questions = null
        $scope.opened= false
        $scope.wizardid = $scope.$id
        $scope.force_close = false
        
        $scope.toggle_bot = ()=>$scope.questions && ($scope.opened=!$scope.opened)
        
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
                
                let next_question = {
                    actions:{options:[{label: 'Yes! please', value:''},{label: 'No! stop!', value: 'goto:last'}]},
                    question :"More questions?",
                    type : "question"
                }
                
                $scope.questions = _(res.data.questions)
                    .map((a, i)=> i>1 && i<res.data.questions.length-1 ? [next_question, a] : [a] )
                    .flatten()
                    .value()
                
                $timeout(function(a){ $scope.opened = true }, 5000)
            }
            else $scope.questions = null
        }
    
        $rootScope.$on('wizard.'+$scope.wizardid+'.end', ()=>{ $rootScope.$emit('chatbot.closed'); $scope.opened=false;  })
        
        $rootScope.$on('wizard.'+$scope.wizardid+'.hide', ()=>{ console.log('hide'); $scope.opened=false; })
        $rootScope.$on('chatbot.force_close', (e, m)=>{ console.log('hide'); $scope.force_close=m; })
        
        $rootScope.$on('authorization.refresh', $scope.get)
 
    
        $scope.entityname = _.get($rootScope, 'page_info.options.entity_name')
        $scope.entityid = _.get($rootScope, 'page_info.options.entity_id')
    
        // Profile page case
        if(
            _.get($rootScope, 'page_info.name') === 'profile_detail' &&
            _.get($rootScope, 'user.profile') != _.get($rootScope, 'page_info.options.profile_id')
        )
        {
            $scope.entityname = 'profile'
            $scope.entityid = _.get($rootScope, 'page_info.options.profile_id')
        }
        
        $scope.get()
    
    }]
}

export default [()=>chatbot_directive]
