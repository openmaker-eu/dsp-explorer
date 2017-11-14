export default ['$http', '$rootScope',  function($http, $rootScope){
    
    let factory = {
        search_filter: '',
        search: (searchString = null, restrict_to = null) => {
            factory.search_filter = searchString || factory.search_filter;
            let options = {
                'method': 'GET',
                'url': searchString ? '/api/v1.1/search/members/'+factory.search_filter : '/api/v1.1/search/last_members/',
            }
            restrict_to && (options.params = { restrict_to : restrict_to })
            let apicall = $http(options)
            apicall.then(
                n=>$rootScope.$emit('user.search.results', n) ,
                n=>$rootScope.$emit('user.search.error', n)
            )
            return apicall
        }
    }
    return factory
    
}]