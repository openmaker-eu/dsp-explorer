let fields = require('../../../templates/question_templates.html')
import {TemplateLoader} from '../../classes/TemplateLoader'

let template = `
     <div ng-form="{$ x.name $}" class="signup-template">
        <div class="" style="padding:5%;">
            <h1 ng-if="x.label" class="signup-template__label">{$ x.label $}</h1>
            <h3 ng-if="x.subtext">{$ x.subtext $}</h3>
            <br>
            <div class="signup-input"></div>
            <h3 ng-if="x.error" class=" signup-template__label text-red">{$ x.error $}</h3>
        </div>
     <div>
`

export default { 
    transclude: true,
    template: template,
    bindings: {
        data: '=',
        model: '=',
    },
    controller: ['$scope', '$element', '$compile', function($scope, $element, $compile) {
        
        // Wait for controller to init
        this.$onInit = ()=>{
            
            // Add binding data to $scope
            $scope.x = this.data
            $scope.m = this.model
            
            // Object containign this sub form
            $scope.subform = $scope[$scope.x.name]
            
            // Compile template
            $scope.$applyAsync(()=>{
                $scope.template = angular.element( TemplateLoader.load(fields, $scope.x.type) )
                $element.find('.signup-input').html( $scope.template )
                $scope.template = $compile( $scope.template )($scope)
            });

        }
        
    }],
}
