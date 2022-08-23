export const zim = ZIM.create(appConfig.appID) as ZIMClass;

zim.queryConversationList({
    count: 100,
})

then((res: any) => {
    console.warn('queryConversationList', res);
    this.convs = res.conversationList;
    return res;
}).catch(on_error);

zim.sendGroupMessage({ message, type: msgType }, convID, { priority: 2 }).catch(on_error);

