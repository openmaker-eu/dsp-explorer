import * as _ from 'lodash'
export default ['$q', function($q){
    var factory = {
        request: function (config) {return config;}
    }
    return factory
}]
