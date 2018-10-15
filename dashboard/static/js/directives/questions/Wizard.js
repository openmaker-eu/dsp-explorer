let _ =  require('lodash')
let template = `
    <h2 class="wizard__close" ng-click="close()" ><i class="fas fa-times text-brown"></i></h2>
    
    <entity-loading
            ng-if="!questions || loading"
            class="text-center"
            loading="true"
            custommessage="{$ loadingmessage $}"
    ></entity-loading>
    
    <form name="wizard.form" ng-if="questions" ng-show="questions && !loading" class="wizard-form" enctype="multipart/form-data">
        <slick class="col-md-12 modal-slider" settings="slickConfig" prev-arrow=".sup-prev" next-arrow=".sup-next">
            <question ng-repeat="question in questions track by $index" data="question" model="wizard.formmodel" ></question>
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
        wizardid : '=',
        configuration : '='
    },
    controller: ['$scope', '$rootScope', '$http', function($scope, $rootScope, $http){
        
        // Models
        $scope.wizard = {form:{}, formmodel:{}}
        $scope.wizard_name = 'wizard.'+($scope.wizardid ||$scope.$id)
        
        // Status variables
        $scope.loading = false
        $scope.loadingmessage = $scope.loadingmessage || 'Loading'
        $scope.error = false
        
        // Slick Carousel configuration
        $scope.slickConfig ={
            method:{},
            slidesToShow: 1, slidesToScroll: 1,
            draggable: false,
            autoplay: false,
            infinite: false,
            adaptiveHeight:true,
            event: {
                afterChange: (event, slick, currentSlide, nextSlide)=>
                    $rootScope.$emit($scope.wizard_name+'.afterChange', {event, slick, currentSlide, nextSlide}),
                init: (event, slick)=>$rootScope.$emit($scope.wizard_name+'.init')
            }
        }
        
        $scope.configuration && ($scope.slickConfig = Object.assign($scope.slickConfig, $scope.configuration))
        
        // Trigger validation and return bool
        $scope.isSubformValid = (subform) => {
            if(!subform || !subform.hasOwnProperty('$$element')) return false
            // Display form errors
            subform.$$element.addClass('subform-submitted')
            // Trigger validation on Next
            _.each(subform.$$controls, (field) => {field.$validate()})
            // Return validation status
            return _.get(subform, '$valid')
        }
        $rootScope.$on($scope.wizard_name+'.next', (ev,current)=>{
            let question = _.get($scope , 'questions['+current+']')
            let subform = question.name && $scope.wizard.form[question.name]
            
            // Go on only if form-data is valid
            if($scope.isSubformValid(subform)) {
                // Perform apicall
                if (question && question.apicall) {
                    $scope.loading = true;
                    
                    // Generate url
                    let url =  question.apicall && _.isString(question.apicall) ? question.apicall : '/api/v1.4/questions/'
                    $scope.action && (url = url + $scope.action + '/')
                    
                    // Create form data
                    let form_data = new FormData( $('.wizard-form')[0] )
                    
                    // SAFARI FIX : Remove picture if empty
                    let picture = form_data.get('picture')
                    picture && picture.size === 0 && form_data.delete('picture')
                    
                    // Post data to backend
                    $http
                        .post(
                            url,
                            form_data,
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
        
        $scope.close = ()=>$rootScope.$emit($scope.wizard_name+'.end', $scope.current)
        
    }]
}

export default [()=>wizard_directive]

