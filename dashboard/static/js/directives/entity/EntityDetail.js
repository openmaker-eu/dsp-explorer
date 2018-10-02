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
            
            $scope.entity.details = $sce.trustAsHtml($scope.entity.details);
            $scope.entity_link = ()=> '/entity/' +
                $scope.entityname + '/' +
                ($scope.entityid || $scope.entity.id || $scope.entity.link_id ) + '/' +
                ($scope.entity.temp_id || '' )
            
            $scope.add_http_to_url = (url)=>url.startsWith("http://") || url.startsWith("https://") ? url : 'http://'+url
    
            const new_image = (src)=>{
                let image = new Image()
                image.src = src
                image.className = "circle-image portrait"
                return image
            }
            
            
            console.log('entity', $scope.entityname);
            
        }]
    }
}]



