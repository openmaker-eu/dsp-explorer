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
            class="col-md-4"
            ng-class="{'col-md-6': question.is_edit}"
        >
            <div class="background-white" style="padding:10%; border:solid 1px #efefef;">
                
                <div
                    class="profile-question__actions"
                    style="position: absolute; top:0; right:0; bottom:0; left:0; width:100%; height:100%;"
                >
                    <h3
                        class="far fa-fw text-red background-white pointer"
                        ng-class="{'fa-eye': !question.is_private, 'fa-eye-slash':question.is_private }"
                        ng-if="!question.feedbacks[1]"
                        style=" position: absolute; top:5%; right:10%;"
                        ng-click="toggle_show(question)"
                    ></h3>
                    <h3
                        class="fas fa-fw fa-edit text-red background-white pointer"
                        style="position: absolute; bottom:10%; right:10%;"
                        ng-click="question.is_edit = !question.is_edit"
                        ng-show="!question.is_edit"
                    ></h3>
                </div>
                
                <h4 class="text-brown">{$ question.question $}</h4>
                <p>{$ question.question_text $}</p>
                
                <hr>
                
                <p ng-if="!question.feedbacks[1]" class="text-red">{$ question.feedbacks[0].label $}</p>
                <p ng-if="question.feedbacks[1]" class="text-brown">
                    <strong>{$ profile.data.user.first_name $}:&nbsp;</strong>&nbsp;&nbsp;{$ question.feedbacks[0].label $}
                </p>
                
                <p ng-if="question.feedbacks[1]" class="text-red">
                    <strong>You:&nbsp;</strong>&nbsp;&nbsp;{$ question.feedbacks[1].label $}
                </p>
                
                <div ng-show="question.is_edit" style="
                    width:100%;
                    display: flex;
                    flex-direction: row;
                    justify-content: space-around;
                    align-items: center;
                    background: #fff;
                    padding:5% 0 0 0;
                    "
                >
                    <div
                        ng-repeat="(act, k) in question.answers"
                        style="padding:1%; z-index:10000;"
                    >
                        <button
                            class="btn btn-danger pull-left capitalize pointer"
                            ng-click="edit_question(question, k)"
                        >{$ act $}</button>
                    </div>
                </div>
               
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
        $scope.wizard_id = $scope.$id;
        $scope.wizard_name = 'wizard.'+$scope.wizard_id;
        
        console.log('profile id', $scope.profileid);
        $scope.get = ()=>{
            $scope.profileid &&
            $http.get(`/api/v1.4/questions/profile?profile_id=${$scope.profileid}`)
                .then((r)=>{$scope.questions = r.data.questions || null})
        }
        
        $scope.get()
        $rootScope.$on('authorization.refresh', ()=>{})
        
        $scope.toggle_show =  async(q)=> {
            let res= await $http.post('/api/v1.4/questions/chatbot/', q)
            q.is_private = !q.is_private
        }
        
        $scope.edit_question = async(question, feedback)=>{
            let q = {...question}
            q.feedback = feedback || q.feedback
            let res= await $http.post('/api/v1.4/questions/chatbot/', q)
            $scope.get()
        }

    }]
}

export default [()=>profile_question_directive]

