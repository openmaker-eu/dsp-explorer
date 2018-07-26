export default function(){
    return {
        template:`
            <i
                ng-click="interest()"
                ng-if="$root.authorization >= 10 && (entityname !== 'projects' || entityname !== 'challenges') "
                class="far pointer"
                ng-class="{
                    'text-highlight': interested,
                    'fa-star':entityname=='projects' || entityname=='challenges',
                    'fa-heart': entityname==='profile',
                    'fa-bookmark': entityname === 'news',
                    'fa-bell': entityname === 'events'
                }"
            ></i>
        `,
        scope: {
            entityname : '@',
            entityid : '@',
            isstatic: '='
        },
        controller : ['$scope', '$http', '$rootScope', 'EntityProvider', '$window', function($scope, $http, $rootScope, EntityProvider, $window){
            $scope.interested = false;
    
            // Build url
            let url=()=> $scope.entityid && `/api/v1.4/user/interest/${$scope.entityname}/${$scope.entityid}/`
    
            // Change bookmarked button color
            const change_status = res => {
                console.log('chage status');
                if(res.status === 200){
                    console.log('chage status success', res);
                    
                    $scope.interested = _.get(res, 'data', $scope.interested)
                    $rootScope.$emit('interested.new')
                    $scope.entityname==='profile' && EntityProvider.entities['lovers'].get(true)
                }
                $rootScope.$emit($scope.entityname+'.'+$scope.entityid+'.interest.change', {'interested':$scope.interested})
            }
    
            $rootScope.$on($scope.entityname+'.'+$scope.entityid+'.interest.change', (e, m)=>$scope.interested = _.get(m, 'interested'))
    
            // First check if is bookmarked
            url() && $http.get(url()).then(change_status)
    
            // Change bookmark on BE OR trigger bookmark action
            $scope.interest = () => {
    
                let is_list = $rootScope.page_info.name == 'entity_list';
                let is_this_entity = $rootScope.page_info.options.entity_name === $scope.entityname;
                console.log('is_list', is_list);
                console.log('is_this_entity', is_this_entity);
                console.log('$scope.isstatic', $scope.isstatic);
                console.log('$scope.entityname', $scope.entityname);
    
                if ( (!is_list || !is_this_entity) && $scope.isstatic){
                    $window.location.href = `/entity/${$scope.entityname}/?bookmark=true`
                }
                else if(!$scope.isstatic){
                    url() && $http.post(url()).then(change_status);
                }
                else{
                    $rootScope.$emit('bookmarked.'+$scope.entityname+'.visibility', {visible:!$scope.interested});
                }

                
            }
            
            // React to bookmark action
            $rootScope.$on('bookmarked.'+$scope.entityname+'.visibility', (e, m)=>{ $scope.interested=m.visible })
            
    
        }]
    }
}
