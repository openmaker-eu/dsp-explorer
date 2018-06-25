let _ = require('lodash')
let $ = require('jquery')

let template = `

    <style>
        .profile-question__actions { display:flex; flex-direction: row; justify-content: flex-end;}
        .profile-question__actions > * { display:none; }
        .profile-question__actions:hover > * { display:block; margin:2%;}
    </style>
    
    <div ng-if="questions" class="profile-questions">
        <div
            ng-repeat="question in questions"
            class="col-md-3"
        >
            <div class="background-white" style="padding:5%; border:solid 1px #efefef;">
                
                <div
                    class="profile-question__actions"
                    style="position: absolute; top:0; right:0; bottom:0; left:0; width:100%; height:100%;"
                >
                    <h3
                        class="far fa-fw text-red background-white pointer"
                        ng-class="{'fa-eye': question.visible, 'fa-eye-slash':!question.visible }"
                        ng-if="!question.feedback[1]"
                        style=" position: absolute; top:5%; right:10%;"
                        ng-click="toggle_show(question)"
                    ></h3>
                    <h3
                        class="fas fa-fw fa-edit text-red background-white pointer"
                        style="position: absolute; bottom:10%; right:10%;"
                        ng-click="edit_question()"
                    ></h3>
                </div>
                
                <h4 class="text-brown">{$ question.question $}</h4>
                <p>{$ question.text $}</p>
                
                <hr>
                
                <p ng-if="!question.feedback[1]" class="text-red">{$ question.feedback[0] $}</p>
                <p ng-if="question.feedback[1]" class="text-brown">
                    <strong>{$ profile.data.user.first_name $}:&nbsp;</strong>&nbsp;&nbsp;{$ question.feedback[0] $}
                </p>
                
                <p ng-if="question.feedback[1]" class="text-red">
                    <strong>You:&nbsp;</strong>&nbsp;&nbsp;{$ question.feedback[1] $}
                </p>
                
            </div>
        
        </div>
    </div>
`

let profile_question_directive =
{
    template:template,
    scope: {
        profile : '='
    },
    controller: ['$scope', '$rootScope', '$http', '$timeout', 'EntityProvider', function($scope, $rootScope, $http, $timeout, EntityProvider){
        
        $scope.profileid = _.get($rootScope, 'page_info.options.profile_id')
        $scope.questions = null
        
        console.log('profile id', $scope.profileid);
        $scope.get = ()=>{
            $scope.profileid &&
            $http.get(`/api/v1.4/questions/profile?profile_id=${$scope.profileid}`)
                .then((r)=>{
                    console.log('PROFILE Q UESTIOONS : ',r);
                    $scope.questions = r.data.questions || null
                })
        }
        
        $scope.get()
    
        $rootScope.$on('authorization.refresh', ()=>{})
        console.log('Profile object', $scope.profile);
        
        $scope.toggle_show = (q)=>{q.visible=!q.visible}
        $scope.edit_question = ()=>{}
    
    }]
}

export default [()=>profile_question_directive]

