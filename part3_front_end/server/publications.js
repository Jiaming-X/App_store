/**
 * Created by jiamingxie on 4/11/16.
 */
Meteor.publish("apps", function (options) {
    return Apps.find({}, options);
});

Meteor.publish("singleApp", function (id) {
    return Apps.find({_id:id});
});

Meteor.publish("singleAppByAppId", function (appId) {
    return Apps.find({app_id:appId});
});

