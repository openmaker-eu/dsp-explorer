import * as _ from 'lodash'
export default ['$http', '$rootScope',  function($http, $rootScope){
    
    var factory = {
        
        search_filter: '',
        text_overwrite:null,
        
        old_search:'',
        restrict_to:'',
        old_restrict_to:'',
        page:null,
        
        is_max_page:false,
        is_min_page:false,
        
        search: (searchString = null, restrict_to = null, page = 1, text_overwrite=null)=>{
            
            factory.text_overwrite = text_overwrite
            factory.search_filter = searchString || factory.search_filter
            
            let options = {
                'method': 'GET',
                'url': '/api/v1.1/search/members/'+factory.search_filter+'/',
                params: {}
            }
    
            restrict_to && (options.params.restrict_to = restrict_to)
            page && (options.params.page = page)
            factory.restrict_to = restrict_to
            
            let apicall = $http(options)
            apicall
                .then(factory.update_context)
                .catch(n=>$rootScope.$emit('user.search.error', n))
            return apicall
            
        },
        
        update_context:(results)=>{
            factory.old_restrict_to = factory.restrict_to
            factory.old_search = factory.search_filter
    
            factory.page = parseInt(results.data.page) || 1
            factory.max_page = results.data.max_page || null
    
            factory.is_min_page = factory.page === 1
            factory.is_max_page = factory.page === factory.max_page
    
            $rootScope.$emit('user.search.results', results)
        },
        
        // Resets class context
        reset_filters:()=>{
            factory.search_filter=''
            factory.old_search=''
            factory.old_restrict_to=''
            factory.page=1
        },
        
        // Same search performed two times in a row resets the search ( useful for buttons )
        search_switch: (...args)=> {
            factory.search_filter = args[0] || factory.search_filter
            factory.search_filter.toLowerCase() === factory.old_search.toLowerCase() && (args[0]=null) || factory.reset_filters()
            factory.search(...args)
        },
        
        search_all:()=>{
            factory.reset_filters()
            factory.search()
        },

        is_search_all:()=> factory.search_filter.trim() === '' ,
        
        // Got to arbitrary page
        // @TODO: check if page exists
        go_to_page: (page=null)=>{ return factory.search(factory.old_search, factory.old_restrict_to, page || 1 ) },
        
        // Go to next page if exist else do nothing
        prev_page: ()=>factory.is_min_page || factory.search(factory.old_search, factory.old_restrict_to, factory.page-1),
        
        // Go to previous page if exist else do nothing
        next_page: ()=>factory.is_max_page || factory.search(factory.old_search, factory.old_restrict_to, factory.page+1)
        
    }
    return factory
    
}]
