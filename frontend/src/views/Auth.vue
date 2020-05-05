<template>
    <amplify-authenticator v-bind:authConfig="authConfig"/>
</template>

<script>
export default {
  data() {
      return {
      authConfig: {
          signUpConfig: {
            hideAllDefaults: true,
            defaultCountryCode: '1',
            signUpFields: [
              {
                label: 'Username',
                key: 'username',
                required: true,
                displayOrder: 1,
                type: 'string',
              },
              {
                label: 'Password',
                key: 'password',
                required: true,
                displayOrder: 2,
                type: 'password'
              },
              {
                label: 'Email',
                key: 'email',
                required: true,
                displayOrder: 3,
                type: 'string'
              }
            ]
          }
        }
      }
  }
};
</script>