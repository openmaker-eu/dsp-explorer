require('../styles/base.scss')

export default function(app){
    
    app.factory('ModalFactory', require('./factories/modal.factory').default )
    app.factory('MessageModal', require('./factories/message.modal.factory').default )
    app.controller('baseController', require('./controllers/base.controller').default )
    
}
