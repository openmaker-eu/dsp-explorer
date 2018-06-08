let _ =  require('lodash')
let template = `
    <entity-loading
            ng-if="!questions || loading"
            class="text-center"
            loading="true"
            custommessage="{$ loadingmessage $}"
    ></entity-loading>
    
    <form name="wizard.form" ng-if="questions" ng-show="questions && !loading" class="wizard-form" enctype="multipart/form-data">
        <slick class="col-md-12 modal-slider" settings="slickConfig" prev-arrow=".sup-prev" next-arrow=".sup-next">
            <question ng-repeat="question in questions" data="question" model="wizard.formmodel" ></question>
        </slick>
    </form>
    
    <div class="col-md-12 step-navigation" ng-show="questions">
        
        <navi-questions ng-if="!action" items="questions" target="$id"></navi-questions>
        
        <div ng-if="action='chatbot.question.simple'" style="display: flex; flex-direction:row; justify-content: center; padding-bottom:3%;">
            <div ng-repeat="act in questions[0].calltoaction" style="padding:1%;">
                <button class="btn btn-danger pull-left" >{$ act.label $}</button>
            </div>
        </div>
        
    </div>
`

let wizard_directive =
{
    template:template,
    scope: {
        questions : '=',
        action : '@',
        loadingmessage : '@'
    },
    controller: ['$scope', '$rootScope', '$http', function($scope, $rootScope, $http){
        // Wizard Unique id
        $scope.wizard_name = 'wizard.'+$scope.$id
        
        // Models
        $scope.wizard = {form:{}, formmodel:{}}
        
        // Status variables
        $scope.loading = false
        $scope.loadingmessage = $scope.loadingmessage || 'Loading your questions'
        $scope.error = false
        
        // Slick Carousel configuration
        $scope.slickConfig ={
            method:{},
            slidesToShow: 1, slidesToScroll: 1,
            draggable: false,
            autoplay: false,
            infinite: false,
            event: {
                afterChange: (event, slick, currentSlide, nextSlide)=>
                    $rootScope.$emit($scope.wizard_name+'.afterChange', {event, slick, currentSlide, nextSlide}),
                init: (event, slick)=>$rootScope.$emit($scope.wizard_name+'.init')
            }
        }
        
        // Trigger validation and return bool
        $scope.isSubformValid = (subform) => {
            // Display form errors
            subform.$$element.addClass('subform-submitted')
            // Trigger validation on Next
            _.each(subform.$$controls, (field) => field.$validate())
            // Return validation status
            return _.get(subform, '$valid')
        }
    
        $rootScope.$on($scope.wizard_name+'.next', (ev,current)=>{
            let question = _.get($scope , 'questions['+current+']')
            let subform = $scope.wizard.form[question.name]
    
            // Go on only if form-data is valid
            if($scope.isSubformValid(subform)) {
                // Perform apicall
                if (question && question.apicall) {
                    $scope.loading = true;
                    $http
                        .post(
                            _.isString(question.apicall) ? question.apicall : '/api/v1.4/questions/',
                            new FormData($('.wizard-form')[0]),
                            {transformRequest: angular.identity, headers: {'Content-Type': undefined}}
                        )
                        .then(res=>{
                            question.emitevent && $rootScope.$emit(question.emitevent, {})
                            $scope.slickConfig.method.slickNext()
                        })
                        .catch(res=>question.error=res.data.error)
                        .finally(()=>$scope.loading=false)
                }
                else $scope.slickConfig.method.slickNext()
            }
            
        })
        $rootScope.$on($scope.wizard_name+'.prev',()=>$scope.slickConfig.method.slickPrev())
        $rootScope.$on($scope.wizard_name+'.end', ()=>$rootScope.$emit('question.modal.close'))
    }]
}

export default [()=>wizard_directive]

