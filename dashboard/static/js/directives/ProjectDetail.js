import * as _ from 'lodash'
import * as d3 from 'd3';


let template = require('../../templates/project_details.html');

export default [function(){
    return {
        template:template,
        scope: { projectid : '=', profileid : '=' },
        controller : ['$scope', '$http', '$window', '$rootScope', '$sce', 'toastr','UserSearchFactory', function($scope, $http, $window, $rootScope, $sce, toastr, UserSearchFactory) {

            $scope.search_factory = UserSearchFactory
            let model_object = 'project'
            $scope.url = '/api/v1.3/project/' + $scope.projectid
            $scope.projects = []
            $scope.results = [];
            $scope.show_form = false
            $scope.show_invite = false


            $scope.search_debounced = () => {
                if ($scope.search_factory.search_filter.length < 3 )
                    $scope.results = []
                else
                    _.debounce($scope.search_factory.search.bind($scope.search_factory.search), 500)()
            }

            $rootScope.$on('user.search.results', (event, results)=>{
                $scope.results = results['data']['result']

                // setting button invitation type to search result
                // ToDo take care of pagination
                if(!_.isEmpty($scope.results))
                    _.forEach($scope.results, (item) => {
                        let match = _.find($scope.project.project_contributors, function(o) { return o.id == item.id; })
                        if (match) item.status = match.status
                    })

                $scope.results_count = results['data']['results_count']
                if ($scope.results_count == 0) $scope.show_invite = true
                $scope.is_last_members_label = $scope.search_factory.search_filter === ''
            })

            $rootScope.$on('user.search.error', (event,data)=>{
                $scope.is_last_members_label = false;
                $scope.results = []
            })

            $scope.highlight = function(text, search) {
                if (!search) {return $sce.trustAsHtml(text);}
                return $sce.trustAsHtml(text.replace(new RegExp(search, 'gi'), '<span class="text-red bold">$&</span>'));
            };

            $scope.clearAll = () => { $scope.results = []; $scope.search_factory.search_filter = ''; $scope.show_invite = false }

            $scope.send_collaborator_invitation = (project_id, profile_id) => {
                // send invitation
                let data = { 'project_id': project_id, 'profile_id': profile_id }
                $http.post('/api/v1.3/project/invitation/', data).then( res => {
                    console.log(res)
                    toastr.success('Success',res.data.message)
                    $scope.search_debounced()
                    $scope.get_data($scope.url)
                },err=>console.log(err))
            }

            $scope.remove_collaborator = (project_id, profile_id) => {
                // remove collaborator
                let status = 'removed'
                let data = { 'project_id': project_id, 'profile_id': profile_id }
                $http.post('/api/v1.3/project/invitation/' + status + '/', data).then(res => {
                    toastr.success('Success',res.data.message)
                    $scope.get_data($scope.url)
                    $scope.$apply(()=>$(window).trigger('resize'))
                },err=>console.log(err))
            }

            $scope.open_close_form = (open_close) => {
                $scope.show_form = open_close
                $scope.clearAll()
            }

            $scope.get_data = (url)=> Promise
                    .all([
                        $http.get(url),
                        $http.get('/api/v1.3/interest/ids/'+model_object)
                    ])
                    .then(
                        res=>{
                            $scope.project = res[0].data.result[0] || []
                            $scope.interested_ids = res[1].data || []
                            $scope.$apply(()=>$(window).trigger('resize'))
                            // flatting contributors
                            // ToDo improve performance
                            if (!_.isEmpty($scope.project.project_contributors))
                                _.forEach($scope.project.project_contributors, function(item) {
                                    _.merge(item, item.contributor);
                                })
                        },
                        err=>console.log('Error: ', err)
                    )

            $scope.delete_project = (url) => {
                $http.delete(url).then(res => {
                    $window.location.href = '/profile';
                    $scope.$apply(()=>$(window).trigger('resize'))
                })
            }

            $scope.get_data($scope.url)

            // set interest
            $scope.click_interest = (project) =>
                ($scope.is_interested(project) ?
                    $http.delete('/api/v1.3/interest/project/'+project.id+'/') :
                    $http.post('/api/v1.3/interest/project/'+project.id+'/')
                )
                .then(res=>$scope.get_data($scope.url),err=>console.log(err))


            // check if logged user is interested or not
            $scope.is_interested = (project) => {
                let result = $scope.interested_ids && $scope.interested_ids.indexOf(project.id) > -1
                return result
            }




        }]
    }
}]



