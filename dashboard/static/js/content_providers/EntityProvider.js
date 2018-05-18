import * as _ from 'lodash'

export default ['$http', '$rootScope',  function($http, $rootScope){
    
    const baseurl = `/api/v1.4`
    
    class Entity {
        data = null
        url = baseurl
        loading = true
        
        constructor(entityname, entityid=null, userid=null) {
            this.entityname = entityname
            this.entityid = entityid
            this.userid = userid
            this.data = entityid ? null : []
            
            this.url += userid ? `/user/${userid}` : ''
            this.url += `/${entityname}/${entityid ? 'details/'+entityid+'/' : ''}`
        }

        get = ()=>{
            this.loading = true;
            let prom = $http.get(this.url, {timeout: 10000})
            prom
                .then(
                    (res)=>{ this.data = res.data, $rootScope.$emit('entitiy.'+this.entityname+'.new')},
                    (err)=>console.log('error', err)
                )
                .finally(()=>this.loading = false)
            return prom
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
    
    const reload_all = (a, b)=>{ a!==b && _.each(f.entities, (e)=>{ e.get() }) }
    
    $rootScope.$watch('authorization', reload_all)
    
    $rootScope.$on('entity.change', (a)=>{_.get(f.entities, a).get()})
    $rootScope.$on('entity.change.all', (a)=>{ reload_all(1,2) })

    return f
    
}]