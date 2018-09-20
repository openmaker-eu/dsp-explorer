let fields = require('../../../templates/question_templates.html')
import {TemplateLoader} from '../../classes/TemplateLoader'

let template = `
     <div ng-form="{$ x.name $}" class="signup-template" style="padding:5%;">
        <div style=" display: flex; flex-direction: column; justify-content: center; align-items: center">
        
            <h1 ng-if="x.label" class="signup-template__label signup-template__title">{$ x.label $}</h1>
            <h4 ng-if="x.question_text" class="text-brown">{$ x.question_text $}</h4>
            <h3 ng-if="x.subtext">{$ x.subtext $}</h3>
            <br>
            
            <!--<div ng-if="!(x.question || x.super_text || x.text)" class="signup-input">-->
            <div class="signup-input" style="width:100%;"></div>
            
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
                
                if( true || $scope.x.type !== 'question') {
                    $scope.template = angular.element( TemplateLoader.load(fields, $scope.x.type) )
                    $element.find('.signup-input').html( $scope.template )
                    $scope.template = $compile( $scope.template )($scope)
                }

            });

        }
        
    }],
}





