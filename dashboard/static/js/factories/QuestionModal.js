import * as _ from 'lodash'


let template = `
   
    <div class="modal-body padding-5-perc">
    
        <entity-loading
                ng-if="loading"
                class="text-center"
                loading="loading"
                entityname=""
                custommessage="Loading your questions"
        ></entity-loading>
        
        <entity-loading
                ng-if="saving"
                class="text-center"
                loading="loading"
                entityname=""
                custommessage="Saving data"
        ></entity-loading>
  
        
            <form name="wizard.form" ng-if="questions" ng-show="!loading" class="wizard-form" enctype="multipart/form-data">
                <slick class="col-md-12 modal-slider" settings="slickConfig" prev-arrow=".sup-prev" next-arrow=".sup-next">
                    <question ng-repeat="question in questions" data="question" model="wizard.formmodel" ></question>
                </slick>
            </form>
           
            <div class="col-md-12 step-navigation" ng-show="!loading">
                
                <span ng-class="{'transparent':is_start}" class="pointer " ng-click="prev()">
                    <h1><i class="fas fa-chevron-left text-brown"></i></h1>
                    <h4>&nbsp;PREVIOUS</h4>
                </span>
               
                <span style="text-align:center;" ng-click="stampa()">
                    <i
                        ng-repeat="(q_index, question) in [].constructor(questions.length) track by $index"
                        class="fa-circle text-brown margin-10-perc"
                        ng-class="{'fas': q_index == current, 'far' :q_index !== current}"
                    ></i>
                </span>
                
                <span ng-if="!is_end" class="pointer" ng-click="next()">
                    <h4>NEXT&nbsp;</h4>
                    <h1><i class="fas fa-chevron-right text-brown"></i></h1>
                </span>
                
                <span ng-if="is_end" ng-click="close()" class="pointer sup-next">
                    <h4>CLOSE&nbsp;&nbsp;</h4>
                    <h1><i class="far fa-times-circle text-brown"></i></h1>
                </span>
                
            </div>

    </div>
`

export default ['$rootScope', '$uibModal', function($rootScope, $uibModal){
    
    let F = {
        open: (ev,preset,action=null)=>{
            
            F.modalInstance = $uibModal.open({
                template: template,
                backdrop: true,
                windowClass: 'signup-modal',
                transclude:true,
                controller: ['$scope', '$http', function($scope, $http){
                    
                    // Models
                    $scope.wizard = {form:{}, formmodel:{}}
                    $scope.questions = preset || null
                    
                    // Status variables
                    $scope.saving = false
                    $scope.loading = !preset
                    $scope.error = false
                    $scope.is_start = true
                    $scope.is_end = false
                    $scope.current = 0;
    
                    // Get questions from backend if not provided to directive
                    !preset && $http
                        .get('/api/v1.4/questions/' + ( action ? '?action='+action : '') )
                        .then((res)=>{
                            $scope.questions = res.data.questions ;
                            $scope.loading = false
                        })
                    
                    // API Call
                    $scope.api_call =(url=false)=>$http.post(_.isString(url) ? url : '/api/v1.4/questions/', $scope.wizard.formmodel)
                    
                    // Go to Next question
                    $scope.next = ()=>{
    
                        let question = _.get($scope , 'questions['+$scope.current+']')
                        let subform = $scope.wizard.form[question.name]
                        
                        // Display form errors
                        subform.$$element.addClass('subform-submitted')
    
                        // Trigger validation on Next
                        _.each(subform.$$controls, (field)=>{field.$validate();})
                        
                        // Go on only if form-data is valid
                        if(_.get(subform, '$valid')) {
                            
                            // Perform apicall
                            if (question && question.apicall) {
                                $scope.saving = true;
                                $http.post(
                                    _.isString(question.apicall) ? question.apicall : '/api/v1.4/questions/',
                                    new FormData($('.wizard-form')[0]),
                                    {transformRequest: angular.identity, headers: {'Content-Type': undefined}}
                                )
                                    .then(() => {
                                        $scope.saving = false;
                                        question.emitevent && $rootScope.$emit(question.emitevent, {})
                                        $scope.slickConfig.method.slickNext()
                                    },
                                    (res) => {
                                        $scope.saving = false;
                                        question.error = res.data.error;
                                    })
                            }
                            else
                                $scope.slickConfig.method.slickNext()
                            
                        }
                    }
                    // Go to Prev question
                    $scope.prev = ()=>{$scope.slickConfig.method.slickPrev()}
    
                    // Close Modal
                    $scope.close = ()=>{ F.modalInstance.close() }
                    
                    // Slick Carousel configuration
                    $scope.slickConfig ={
                        method:{},
                        slidesToShow: 1, slidesToScroll: 1,
                        draggable: false,
                        autoplay: false,
                        infinite: false,
                        event: {
                            afterChange: function (event, slick, currentSlide, nextSlide) {
                                $scope.current = currentSlide;
                                $scope.is_start = currentSlide === 0
                                $scope.is_end = currentSlide+1 === $scope.questions.length
                                $('.slick-current').find('input, select').first().focus().select().click()
                                
                            },
                            init: function (event, slick) {
                                slick.slickGoTo($scope.current);
                            }
                        }
                    }
    
                    window.onkeypress = (e)=> { e.which=== 13 && $scope.next()}
                    $scope.stampa = ()=>{console.log($scope.wizard.form) ; console.log($scope.wizard.formmodel)}
    
                }]
            });
        }
    }
    
    $rootScope.$on('question.modal.open', F.open)
    return F
    
}]