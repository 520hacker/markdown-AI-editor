<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  width: {
    type: [Number, String],
    default: 18,
  },
  height: {
    type: [Number, String],
    default: 18,
  },
});
</script>
<template>
  <svg
    data-v-01a48685=""
    :width="width"
    :height="height"
    fill="none"
    viewBox="0 0 12 12"
    style="min-width: 16px; min-height: 16px">
    <g data-v-01a48685="">
      <path
        data-v-01a48685=""
        data-follow-fill="currentColor"
        d="M5.143 2.571c0-.428-.429-.857-.857-.857-.429 0-.857.429-.857.857 0 .43.428.858.857.858.428 0 .857-.429.857-.857ZM6.857 9.43c0 .428.429.857.857.857.429 0 .858-.429.858-.857 0-.429-.429-.857-.858-.857-.428 0-.857.428-.857.857Zm1.715-6.857c0-.43-.429-.858-.858-.858-.428 0-.857.429-.857.857 0 .43.429.858.857.858.429 0 .858-.429.858-.857ZM5.143 9.428c0-.429-.429-.857-.857-.857-.429 0-.857.428-.857.857 0 .428.428.857.857.857.428 0 .857-.429.857-.857ZM8.572 6c0-.428-.429-.857-.858-.857-.428 0-.857.429-.857.857 0 .429.429.857.857.857.429 0 .858-.428.858-.857ZM5.143 6c0-.428-.429-.857-.857-.857-.429 0-.857.429-.857.857 0 .429.428.857.857.857.428 0 .857-.428.857-.857Z"
        fill="currentColor"></path>
    </g>
  </svg>
</template>
