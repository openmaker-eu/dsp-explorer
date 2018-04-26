import * as _ from 'lodash'

export default ['$http', '$rootScope',  function($http, $rootScope){
    
    const baseurl = `/api/v1.4`
    
    class Entity {
        data = null
        url = ''
        
        constructor(entityname, entityid=null) {
            this.entityname = entityname
            this.entityid = entityid
            this.data = entityid ? null : []
            this.url = `${baseurl}/${entityname}/${entityid ? 'details/'+entityid+'/' : ''}`
        }

        get = async ()=>{
            console.log('get', this.url);
            this.data = (await $http.get( this.url, {timeout: 5000}) ).data || this.data
            return await this.data
        }
    }
    
    let f = {
        entities : {},
        make(entityname, entityid=null) {
            let name = entityname + ( entityid ? '_detail_'+entityid : '' )
            f.entities.hasOwnProperty(name) || ( f.entities[name] = new Entity(entityname, entityid) )
            return f.entities[name]
        }
    }
    
    $rootScope.$on('authorization.change', (a,b)=>{
        if(a!==b) {
            console.log('change');
            _.each(f.entities, (e)=>{ e.get() })
        }
    })

    return f
    
}]