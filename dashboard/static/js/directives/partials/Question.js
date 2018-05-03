let fields = require('../../../templates/question_templates.html')
import {TemplateLoader} from '../../classes/TemplateLoader'

let template = `
     <form name="{$ x.name $}" class="signup-template">
        <div class="" style="padding:5%;">
            <h1 class="signup-template__label">{$ x.label $}</h1>
            <br>
            <div class="signup-input"></div>
            <h3 ng-if="x.error" class=" signup-template__label text-red">{$ x.error $}</h3>
        </div>
        <input type="submit" class="submit" style="display:none!important;">
     <form>
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
            $scope[$scope.x.name] = {}
            
            $scope.template = angular.element( TemplateLoader.load(fields, this.data.type) )
            $element.find('.signup-input').html( $scope.template )
    
            // Compile template
            $scope.$applyAsync(function() {
                $scope.template = $compile( $scope.template )($scope)
            });

        }
        
    }],
}
