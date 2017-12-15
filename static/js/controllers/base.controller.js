import * as _ from 'lodash'
export default
    ['$scope','$uibModal','$http','$rootScope','toastr','MessageModal', 'ModalFactory',
    function ($scope,$uibModal,$http,$rootScope,toastr, MessageModal, ModalFactory) {
    
    $scope.rootScope = $rootScope;
    
    $scope.openModal = (m) => {
        let modal = $(m);
        if( modal.length>0 ){
            $scope.modalInstance = $uibModal.open({
                template: modal.html(),
                backdrop: 'static',
                scope: $scope
            });
        }
    }
    
    $scope.closeModal = () => { $scope.modalInstance.close();  $scope.modal_message = null;}
    
    $scope.modal_message = null;
    
    $scope.$watch('toastrMessage', function (newValue, oldValue) {
        _.forEach( newValue, (el) => {
            
            el.tags = el.tags.split(" ")
            let toastr_tags = [ 'debug', 'info', 'success', 'warning', 'error' ]
            
            // Is a Modal
            if( el.tags.indexOf('modal') > -1 ){
                try{

                    console.log(el.message);

                    let modal_options = JSON.parse( el.message );
                    modal_options.body = modal_options.body.replace(/ESCAPE/g, '"');
                    modal_options.title
                        && modal_options.body
                        && MessageModal.openModal(
                            modal_options.title || null,
                            modal_options.body || null,
                            null,
                            null,
                            null,
                            modal_options.footer
                        )
                }
                catch(e){console.log('[ERROR] : modal message object is not valid');}
                return
            }
            // Is a Toastr
            else
            {
                _.forEach(el.tags, (tag)=>{
                    let tag_index = toastr_tags.indexOf(tag)
                    if(tag_index > -1) toastr[toastr_tags[tag_index]](el.message);
                })
            }
            
        })
    })
    
    var push_footer =()=>{
        console.log('rendering');
        $('#top-div').css('height', 'auto')
    
        var header_padding = 30;
        var header_margin = 20;
        var header_border = 1;
    
        var height_needed = $(".navbar").height() + header_padding + header_margin + header_border
        var spacer = $("#spacer").length === 0 ? $('<div id="spacer"></div>').prependTo("body") : $("#spacer")
    
        spacer.css("height", height_needed)
    
        var body_height = $('body').height();
        var content_height = $('#top-div').height();
        var footer_height = $('#footer').height();
    
        if((height_needed + content_height + footer_height) < body_height) {
            $('#top-div').height(body_height - height_needed - footer_height)
        }
    }
    
    $scope.re_render =()=>{push_footer()}
    
    $(window).on('resize', $scope.re_render);
    $(document ).ready($scope.re_render)
    
    $scope.$watch(()=>$scope.$$postDigest(()=>$scope.re_render()))

}]

