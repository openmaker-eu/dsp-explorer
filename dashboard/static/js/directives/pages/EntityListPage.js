import * as _ from 'lodash'

let template = require('./templates/EntityListPage.html')

export default [function(){
    return {
        template:template,
        scope: {
            profileid : '=',
            entityname : '@',
            slider : '@'
        },
        controller : ['$scope', '$http', '$rootScope', 'EntityProvider', '$timeout', function($scope, $http, $rootScope, EntityProvider, $timeout) {
            
            // PAGINATION
            $scope.page = 0
            $scope.nextcursor = _.get($scope.entities, 'is_last_page')
            $scope.prevcursor = -1
            $scope.force_loading = false
            
            $scope.prev=()=>{
                $scope.page = $scope.page-1
                $scope.get_data()
            }
            
            $scope.next=()=>{
                $scope.page = $scope.page+1
                $scope.get_data()
            }
            
            $scope.get_data = ()=>{
                $scope.force_loading = true
                var response = $scope.entities.get(true , $scope.page)
                response.then((res)=>{
                    $scope.nextcursor = _.get($scope.entities, 'is_last_page') ? 0: 1
                    $scope.prevcursor = $scope.page
                    $scope.force_loading = false
                })
                return response
            }
    
            
            $scope.entities = EntityProvider.make($scope.entityname)
            $scope.data = $scope.get_data()
            $scope.nodata = !$scope.data
            
            $scope.data.then(
                ()=> $timeout(function(a){
                    $rootScope.$emit(`bookmarked.${$scope.entityname}.visibility`, {visible:$rootScope.page_info.bookmark})
                },1000)
            )
    
            // $rootScope.$emit(`bookmarked.${$scope.entityname}.visibility`, {visible:true})
            $scope.entitiy_title= ()=> ['challenges', 'projects'].includes($scope.entityname)
                ? '<span>Projects</span><span></span>&nbsp;/&nbsp;</span><span class="text-yellow">Challenges</span>'
                : $scope.entityname == 'news' ? 'articles' : $scope.entityname
    
        }]
    }
}]





