export default function(){
    return {
        template:`
        <i
            ng-click="bookmark()"
            ng-if="$root.authorization >= 10"
            class="far pointer"
            ng-class="
                {'text-highlight': bookmarked, 'visible fa-bookmark': entityname === 'news', 'visible fa-bell': entityname === 'events'}"
        ></i>
`,
        scope: {
            entityname : '@',
            entityid : '@',
            isstatic:'='
        },
        controller : ['$scope', '$rootScope', '$http', '$window', function($scope, $rootScope, $http, $window){
            // Default bookmarked status
            $scope.bookmarked = false;
            // Build url
            let url = ()=>`/api/v1.4/bookmark/${$scope.entityname}/${$scope.entityid}/`
            
            // Change bookmarked button color
            const change_status = res => {
                if(res.status === 200) {
                    $scope.bookmarked = _.get(res, 'data', $scope.bookmarked)
                }
                $rootScope.$emit($scope.entityname+'.'+$scope.entityid+'.bookmark.change', {'interested':$scope.bookmarked})
            }
            $rootScope.$on($scope.entityname+'.'+$scope.entityid+'.bookmark.change', (e, m)=>$scope.bookmarked = _.get(m, 'interested'))
    
            // First check if is bookmarked
            $http.get(url()).then(change_status)
            
            // Change bookmark on BE
            $scope.bookmark = () =>{
    
                let is_list = $rootScope.page_info.name == 'entity_list'
                //let is_detail = $rootScope.page_info.name == 'entity_detail'
                let is_this_entity = $rootScope.page_info.options.entity_name == $scope.entityname
    
                (!is_list || !is_this_entity) && $scope.isstatic && ( $window.location.href = `/entity/${$scope.entityname}`)
                
                (!$scope.isstatic) && $http.post(url()).then(change_status)
                
                $scope.isstatic && $rootScope.$emit('bookmarked.'+$scope.entityname+'.visibility', {visible:!$scope.bookmarked})
                
            }
    
            // React to bookmark action
            $rootScope.$on('bookmarked.'+$scope.entityname+'.visibility', (e, m)=>{ $scope.bookmarked=m.visible })

            
        }]
    }
}
