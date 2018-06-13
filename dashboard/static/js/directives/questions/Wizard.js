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
`

let wizard_directive =
{
    template:template,
    scope: {
        questions : '=',
        action : '@',
        loadingmessage : '@',
        wizardid : '='
    },
    controller: ['$scope', '$rootScope', '$http', function($scope, $rootScope, $http){
        
        // Models
        $scope.wizard = {form:{}, formmodel:{}}
        $scope.wizard_name = 'wizard.'+($scope.wizardid ||$scope.$id)
        
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
            if(!subform || !subform.hasOwnProperty('$$element')) return false
            // Display form errors
            subform.$$element.addClass('subform-submitted')
            // Trigger validation on Next
            _.each(subform.$$controls, (field) => field.$validate())
            // Return validation status
            return _.get(subform, '$valid')
        }
    
        $rootScope.$on($scope.wizard_name+'.next', (ev,current)=>{
            
            console.log('WIZARD: ', $scope.wizardid);
            console.log('WIZARD ACTION: ', $scope.action);
            
            let question = _.get($scope , 'questions['+current+']')
            let subform = $scope.wizard.form[question.name]
            
            // Go on only if form-data is valid
            if($scope.isSubformValid(subform)) {
                // Perform apicall
                if (question && question.apicall) {
                    $scope.loading = true;
                    let url =  _.isString(question.apicall) ? question.apicall : '/api/v1.4/questions/'
                    $scope.action && (url = url + $scope.action + '/')
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
                else { question.emitevent && $rootScope.$emit(question.emitevent, {}) ; $scope.slickConfig.method.slickNext() }
            }
            else if($scope.action==='chatbot'){
                $http
                    .post('/api/v1.4/questions/chatbot/', question)
                    .then(res=>{$scope.slickConfig.method.slickNext()})
                    .catch(res=>question.error=res.data.error)
                    .finally(()=>$scope.loading=false)
            }
            
        })
        
        $rootScope.$on($scope.wizard_name+'.prev',()=>$scope.slickConfig.method.slickPrev())
        $rootScope.$on($scope.wizard_name+'.goto',(ev,val)=>$scope.slickConfig.method.slickGoTo(val))
        $rootScope.$on($scope.wizard_name+'.end', ()=>null)
        
    }]
}

export default [()=>wizard_directive]

