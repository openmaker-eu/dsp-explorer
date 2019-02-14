let template = require('./templates/EntityDetails.html')

export default [function(){
    return {
        template:template,
        scope: {
            entity: '=',
            entityname: '@',
            entityid : '@',
            preview : '='
        },
        controller : ['$scope', '$sce', function($scope, $sce) {
            
            // @TODO: link is broken entitiname is mess whe is project/challenge...
            $scope.entity.details = $sce.trustAsHtml($scope.entity.details);
            console.log('name',$scope.entityname);
            
            let plurals = ['news']
            
            
            const singularize = (name)=>
                plurals.includes($scope.entityname) ?
                    $scope.entityname :
                    $scope.entityname.slice(0, -1)
            
            $scope.entity_link = ()=> '/entity/' +
                $scope.entityname + '/' +
                ($scope.entityid || $scope.entity.id || $scope.entity.link_id ) + '/' +
                ($scope.entity[`${singularize($scope.entityname)}_id`] || '' )
            
            $scope.add_http_to_url = (url)=>url.startsWith("http://") || url.startsWith("https://") ? url : 'http://'+url
    
            const new_image = (src)=>{
                let image = new Image()
                image.src = src
                image.className = "circle-image portrait"
                return image
            }
            
        }]
    }
}]



