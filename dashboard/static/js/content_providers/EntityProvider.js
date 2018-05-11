import * as _ from 'lodash'

export default ['$http', '$rootScope',  function($http, $rootScope){
    
    const baseurl = `/api/v1.4`
    
    class Entity {
        data = null
        url = baseurl
        
        constructor(entityname, entityid=null, userid=null) {
            this.entityname = entityname
            this.entityid = entityid
            this.userid = userid
            this.data = entityid ? null : []
            
            this.url += userid ? `/user/${userid}` : ''
            this.url += `/${entityname}/${entityid ? 'details/'+entityid+'/' : ''}`
        }

        get = async ()=>{
            this.data = (await $http.get( this.url, {timeout: 5000}) ).data || this.data
            return await this.data
        }
    }
    
    let f = {
        entities : {},
        make(entityname, entityid=null, userid=null) {
            let name = entityname + ( entityid ? '_detail_'+entityid : '' )
            f.entities.hasOwnProperty(name) || ( f.entities[name] = new Entity(entityname, entityid, userid) )
            return f.entities[name]
        }
    }
    
    $rootScope.$watch('authorization', (a,b)=>{
        if(a!==b) {_.each(f.entities, (e)=>{ e.get() })}
    })

    return f
    
}]