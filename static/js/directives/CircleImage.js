let placeholder = '/media/images/profile/other.svg'

let template = `
    <a ng-href="{$ href $}" style="display: block;">
        <div class="profile-image-static background-grey" ng-class="{'squared': squared }">
            <img ng-if="!src" ng-src="{$ placeholder $}" class="circle-image landscape" alt="">
        </div>
    </a>

    <style>
        .profile-image-static { overflow: hidden; z-index:1000;}
        .not-pointer , .not-pointer *{ cursor:default!important; }
        .circle-image { position:absolute; }
        .portrait { height:100%!important; width:auto!important;  }
        .landscape { width:100%!important; height:auto!important; }
    </style>
`

export default {
    transclude: true,
    template: template,
    bindings: {
        src: '<',
        href: '@',
        squared: '<',
        placeholder: '@'
    },
    controller: ['$scope', '$element', '$compile', function($scope, $element, $compile) {
        
        this.$onChanges = function(changes){
            
            $scope.src= changes.src && changes.src.currentValue || undefined
            $scope.href= (changes.href && changes.href.currentValue) || undefined
            $scope.squared= this.squared
            $scope.placeholder= (changes.placeholder && changes.placeholder.currentValue) || placeholder
            
            $scope.loaded = false
            
            const new_image = (src)=>{
                let image = new Image()
                image.src = src
                image.className = "circle-image portrait"
                return image
            }
            
            const create_image = ()=>{
                
                let image = new_image($scope.src)
                console.log('squared', this.squared);
    
                image.addEventListener('load', p=> {
                    console.log('load image', $scope.src);
                    p.target.height > p.target.width && (image.className = "circle-image landscape")
                    $element.find('.profile-image-static').html(image)
                    $scope.loaded = true
                })
                image.addEventListener('error', ()=> {
                    $scope.loaded === false &&
        
                    $element.find('.profile-image-static').html(new_image($scope.placeholder || placeholder))
        
                })
                
                
            }
            
            $scope.src && create_image()
            
        };
        
    }],
}
