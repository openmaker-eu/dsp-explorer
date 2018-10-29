export default function(){
    return {
        template:`
        <div ng-if="$root.authorization >= 10 && (entityname !== 'projects' || entityname !== 'challenges') "
            ng-click="interest()" class="far pointer text--darken--hover" ng-class="{
            'text-highlight': interested}"> 
                <i ng-if="entityname==='challenges'" ng-class="{
                    'text-highlight': interested}" class="cairo"> 
                Apply</i>
                <i
                class="far pointer text--darken--hover"
                ng-class="{
                'text-highlight': interested,
                'fa-star':entityname==='projects' || entityname==='challenges',
                'fa-heart': entityname==='profile',
                'fa-bookmark': entityname === 'news',
                'fa-bell': entityname === 'events'
                }"
                ></i>
        </div>     
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
                if(res.status === 200){
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
    
                //let is_list = $rootScope.page_info.name == 'entity_list';
                //let is_this_entity = _.get($rootScope, 'page_info.options.entity_name') === $scope.entityname;
                // if ( (!is_list || !is_this_entity) && $scope.isstatic){
                //     $window.location.href = `/entity/${$scope.entityname}/?bookmark=true`
                // }
                // else
                if(!$scope.isstatic){ url() && $http.post(url()).then(change_status); }
                else{ $rootScope.$emit('bookmarked.'+$scope.entityname+'.visibility', {visible:!$scope.interested}); }

                console.log("ciao")
            }
            
            // React to bookmark action
            $rootScope.$on('bookmarked.'+$scope.entityname+'.visibility', (e, m)=>{ $scope.interested=m.visible })
            
            
        }]
    }
}
