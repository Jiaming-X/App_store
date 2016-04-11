/**
 * Created by jiamingxie on 4/11/16.
 */
Template.appPage.helpers({
    getSuggestedApp: function(appId) {
        Meteor.subscribe('singleAppByAppId', appId);
        return Apps.findOne({app_id: appId});
    }
});

Template.appPage.events({
    "click #backLink" : function(evt) {
        history.back();
    }
});
