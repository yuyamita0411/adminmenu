FROM node:latest

RUN npm install --global @vue/cli

WORKDIR /templates

RUN npm install vue-router@next && npm install vue-class-component@next && npm install lodash --save && npm install vue-property-decorator && npm install vuex --save && npm install vuex@next

RUN npm install eslint eslint-plugin-vue --save-dev

RUN npm install @vue/eslint-config-typescript --save-dev

#RUN npm install @typescript-eslint/parser @typescript-eslint/eslint-plugin --save-dev

#npm install vue-router@next
#npm install vue-class-component@next
#npm install lodash --save
#npm install vue-property-decorator
#npm install vuex --save
#npm install vuex@next


#docker container ls -a | grep "admin_" | awk '{print $1}' | xargs docker rm -f
#docker rmi $(docker images |grep admin_)