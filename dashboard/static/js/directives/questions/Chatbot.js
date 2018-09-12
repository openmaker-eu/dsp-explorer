let _ = require('lodash')
let $ = require('jquery')
let moment = require('moment')

let template = `
    <div class="chatbot">
        <div class="chatbot__container">
            
            <div class="chatbot__header mobile__padding" >
                <h2 class="chatbot__header__flex">
                    <div class="entity-actions" ng-if="$root.authorization >= 10">
                        <a
                            tooltip-popup-delay="{$ tooltip_delay $}"
                            tooltip-append-to-body="true"
                            uib-tooltip-html="tooltip_html('news')"
                            href="/entity/news/?bookmark=true"
                            class="far fa-bookmark pointer text--darken--hover" ng-class="{'text-highlight': $root.bookmarks.news}"
                        ></a>
                        <a
                            tooltip-popup-delay="{$ tooltip_delay $}"
                            tooltip-append-to-body="true"
                            uib-tooltip-html="tooltip_html('projects')"
                            href="/entity/projects/?bookmark=true"
                            class="far fa-star pointer text--darken--hover" ng-class="{'text-highlight': $root.bookmarks.projects}"
                        ></a>
                        <a
                            tooltip-popup-delay="{$ tooltip_delay $}"
                            tooltip-append-to-body="true"
                            uib-tooltip-html="tooltip_html('events')"
                            href="/entity/events/?bookmark=true"
                            class="far fa-bell pointer text--darken--hover" ng-class="{'text-highlight': $root.bookmarks.events}"
                        ></a>
                    </div>
                    <div class="chatbot__toggler pointer">
                        <span
                            tooltip-popup-delay="{$ tooltip_delay $}"
                            tooltip-append-to-body="true"
                            uib-tooltip-html="opened ?'<big>Close me!</big>': '<big>Talk with me!</big>' "
                            class="fas fa-chevron-up text-white"
                            ng-class="{'fa-chevron-down':opened && !force_close, 'fa-chevron-up':!opened || force_close}"
                            ng-click="user_toggle_bot()"
                        ></span>
                    </div>
                </h2>
            </div>
            <div class="chatbot__body" ng-if="opened && !force_close" style="background: white; padding-bottom:36px;">
                <wizard
                    questions="questions"
                    action="chatbot"
                    loadingmessage="I'm writing"
                    wizardid="wizardid"
                    configuration="{verticalSwiping:true, cssEase:false}"
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
    controller:
        ['$scope', '$rootScope', '$http', '$timeout', 'EntityProvider', '$cookies',
        function($scope, $rootScope, $http, $timeout, EntityProvider, $cookies)
    {
        
        // VARS
        $scope.questions = null
        $scope.opened= false
        $scope.wizardid = $scope.$id
        $scope.force_close = false
        $scope.entityname = _.get($rootScope, 'page_info.options.entity_name') || 'profile'
        $scope.entityid = _.get($rootScope, 'page_info.options.entity_id') || _.get($rootScope, 'page_info.options.profile_id')
        $scope.tooltip_delay = 900
        
        /*
        *  NETWORK FUNCTIONS
        * */
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
            if(page_options && page_options.hasOwnProperty('entity_name')){
                url += '?entity_name='+page_options['entity_name']
                page_options.hasOwnProperty('entity_id') && (url += '&entity_id='+page_options['entity_id'])
                page_options.hasOwnProperty('entity_temp_id') && (url += '&entity_temp_id='+page_options['entity_temp_id'])
            }
            return url
        }
        $scope.handle_response = (res)=>{
            
            console.log('CAHTBOT', res);
            
            if(_.isArray(res.data.questions) && res.data.questions.length > 0) {
                
                let next_question = {
                    actions:{options:[{label: 'Yes! please', value:''},{label: 'No! stop!', value: 'goto:last'}]},
                    question :"More questions?",
                    type : "question"
                }
                
                $scope.questions = _(res.data.questions)
                    .map((a, i)=> i>1 && i<4 && i<res.data.questions.length-1 ? [next_question, a] : [a] )
                    .flatten()
                    .value()
                
                $timeout(function(a){
                    $scope.should_open() &&
                    ($scope.opened = true) &&
                    $cookies.putObject('chatbot_last_open_date', moment())
                }, 0)
                
            }
            else $scope.questions = null
        }
    
        $scope.get()
    
    
        /*
        *  MESSAGES HANDLERS
        * */
        $rootScope.$on('wizard.'+$scope.wizardid+'.end', ()=>{ $rootScope.$emit('chatbot.closed'); $scope.opened=false;  })
        $rootScope.$on('wizard.'+$scope.wizardid+'.hide', ()=>{ $scope.opened=false; })
        $rootScope.$on('chatbot.force_close', (e, m)=>{ $scope.force_close=m; })
        $rootScope.$on('chatbot.dont_bother_me', ()=>$scope.dont_bother_me())
        $rootScope.$on('authorization.refresh', ()=>$scope.get())
        $rootScope.$on('interested.new', ()=>{
            $http
                .get('/api/v1.4/interest/chatbot/')
                .then(res=>res.data && res.status === 200 && ($rootScope.bookmarks = res.data))
                .catch(e=>console.log(e))
        })
        
        
        /*
        *  TEMPLATE FUNCTIONS
        * */
        $scope.tooltip_html = (entity_name)=>{
            let bookmarks = _.get($rootScope, `bookmarks.${entity_name}`);
            let entity_label = entity_name == 'news' ? 'articles': entity_name
            return `
                <big>
                    You have ${ bookmarks ? bookmarks+' Bookmarked '+entity_label : 'not bookmarked any '+entity_label+' yet'}
                    <br>Click the icon to go to the ${entity_label} page
                </big>
            `
        }
        
        /*
        *  OPEN/CLOSE LOGIC
        * */
        $scope.user_toggle_bot = ()=> {
            if($scope.opened==='by_user') $scope.opened=false
            else if($scope.opened===true) {$scope.dont_bother_me(); $scope.opened=false; }
            else if($scope.opened===false) $scope.opened='by_user'
            return $scope.questions && $scope.opened
        }
    
        $scope.should_open = ()=> {
        
            let time_format = 'YYYY-MM-DDTHH:mm:ss.SSSSZ'
            let time = $rootScope.authorization >=10 ? 0 : 3;
        
            let last_open = $cookies.getObject('chatbot_last_open_date')
            let bother = $cookies.getObject('chatbot_dont_bother_date')
        
            let is_page_blacklisted = !['project_create_update', 'invite', 'reset_pwd', 'recover_pwd'].includes(_.get($rootScope , 'page_info.name'))
            let is_date_ok = !last_open || moment(last_open, time_format).isBefore(moment().subtract(time, 'minutes'))
                && !bother || moment(bother, time_format).isBefore(moment().subtract(1, 'days'))
        
            return is_page_blacklisted && is_date_ok && $scope.questions.length !== 1
        }
        
        $scope.dont_bother_me = ()=>{console.log('dont bother me');  return $cookies.putObject('chatbot_dont_bother_date', moment()) }
    
    }]
}

export default [()=>chatbot_directive]

