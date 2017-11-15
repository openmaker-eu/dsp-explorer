export default ['$http', '$rootScope',  function($http, $rootScope){
    
    let factory = {
        
        search_filter: '',
        old_search:'',
        old_restrict_to:'',
        page:null,
        is_max_page:false,
        is_min_page:false,
        
        search: (searchString = null, restrict_to = null, page = 1,force_change=false) => {
            
            factory.search_filter = searchString || factory.search_filter;
    
            let nochange = !force_change && (factory.search_filter.toLowerCase() === factory.old_search.toLowerCase())

            if(nochange){
                factory.search_filter=''
                factory.searchString=''
                factory.old_search=''
                factory.old_restrict_to=''
                factory.page=1
            }
            
            factory.old_restrict_to = restrict_to
            factory.old_search = factory.search_filter
    
            let options = {
                'method': 'GET',
                'url': '/api/v1.1/search/members/'+factory.search_filter+'/',
                params: {}
            }
            
            restrict_to && (options.params.restrict_to = restrict_to)
            page && (options.params.page = page)
            
            let apicall = $http(options)
            
            apicall.then(
                n=>{
                    $rootScope.$emit('user.search.results', n)
                    factory.page = parseInt(n.data.page) || 1
                    factory.max_page = n.data.max_page
    
                    factory.is_min_page = factory.page === 1
                    factory.is_max_page = factory.page === factory.max_page
                },
                n=>$rootScope.$emit('user.search.error', n)
            )
            return apicall
        },
        
        go_to_page: (page=null)=>{ return factory.search(factory.old_search, factory.old_restrict_to, page || 1 ) },
        prev_page: ()=>{ return factory.search(factory.old_search, factory.old_restrict_to, factory.page-1 , true) },
        next_page: ()=>{ return factory.search(factory.old_search, factory.old_restrict_to, factory.page+1 , true) }
        
    }
    return factory
    
}]