let _ = require('lodash')
let $ = require('jquery')

let template = `
    <div ng-if="questions" class="profile-questions">
        <div
            ng-repeat="question in questions"
            class="col-md-4"
        >
            <div class="background-white" style="padding:5%; border:solid 1px #bbb;">
                
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
    
    }]
}

export default [()=>profile_question_directive]

