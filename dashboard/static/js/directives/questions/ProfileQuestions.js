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
                <p>{$ question.feedback[0] $}</p>
            </div>
        
        </div>
    </div>
`

let profile_question_directive =
{
    template:template,
    scope: {},
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
    
    
    }]
}

export default [()=>profile_question_directive]

