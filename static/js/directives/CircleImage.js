let template = `
    <a ng-href="{$ href $}" style="display: block;">
        <div class="profile-image-static background-grey"></div>
    </a>

    <style>
        .profile-image-static { border-radius:50%; overflow: hidden; z-index:1000;s}
        .not-pointer , .not-pointer *{ cursor:default!important; }
        .circle-image { position:absolute; }
        .landscape { height:100%!important; width:auto!important;  }
        .portrait { width:100%!important; height:auto!important; }
    </style>
`

export default {
    transclude: true,
    template: template,
    bindings: {
        src: '<',
        href: '@'
    },
    controller: ['$scope', '$element', '$compile', function($scope, $element, $compile) {
        
        this.$onChanges = function(changes){
            $scope.src= changes.src && changes.src.currentValue || undefined
            $scope.href= (changes.href && changes.href.currentValue) || undefined
            
            let image = new Image()
            image.src = $scope.src
            image.className = "circle-image landscape"
            
            image.onload = p=> p.target.height > p.target.width && (image.className = "circle-image portrait")
            
            $element.find('.profile-image-static').html(image)
            
        };
        
    }],
}