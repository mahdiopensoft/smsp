<template>
  <v-row>
    <v-col cols="12" md="8">
      <v-row class="pa-2">
        <Fields
          :data="data"
          :fields="fields.filter((e) => e.group === 'Information Basic')"
          :attr="{
            fk_country: {
              ...paramLocation.fk_country,
              update: () => changeName(),
              disabled: originData.fk_country,
            },
            fk_governorate: {
              ...paramLocation.fk_governorate,
              param: data.fk_country,
              selectObject: (val, obj) => changeName(val, obj),
              disabled: originData.fk_governorate,
            },
            fk_directorate: {
              ...paramLocation.fk_directorate,
              param: data.fk_governorate,
              selectObject: (val, obj) => changeName(val, obj),
              disabled: originData.fk_directorate,
            },
            fk_region: {
              ...paramLocation.fk_region,
              param: data.fk_directorate,
              selectObject: (val, obj) => changeName(val, obj),
              disabled: originData.fk_region,
            },
            url: {
              depend: data.id,
            },
            fk_parent_organization: {
              param: data.company_level,
              depend:
                originData.fk_parent_organization == 0 && state.organization_id == 0,
            },
            type_of_main_system: {
              param: data.company_level,
              default: '',
            },
          }"
        >
          <template v-slot="{ field }">
            <template v-if="field.name === 'company_level'">
              <auto-list
                v-model="data.company_level"
                name="CompanyLevelFilterChoices"
                cols="4"
                :param="paramCompanyLevel"
                @update:modelValue="emit('changeCompanyLevel')"
                :disabled="
                  originData.fk_organization != 0 ||
                  (originData.fk_parent_organization != 0 &&
                    originData.company_level != 30)
                "
              >
                <template v-slot:append-inner> </template>
              </auto-list>
              <VIcon
                class="mt-4"
                icon="mdi-refresh"
                color="error"
                @click="emit('changeCompanyLevel')"
                v-if="errorLevel"
              />
            </template>
          </template>
        </Fields>
      </v-row>
    </v-col>
    <VCol cols="12" md="4" class="pa-2 justify-items-center">
      <CustomImage
        v-if="hasLevel(levels.COMPANY, levels.COLLEGE)"
        v-model="data.logo"
        :title="$t('logo')"
      />
    </VCol>
  </v-row>
</template>

<script setup>
import { ref } from "vue";
import api from "../../../../../plugins/axios-plugin";
import { state } from "@/../src/store/state";

const props = defineProps({
  fields: {
    type: Array,
    default: [],
  },
  levels: {
    type: Object,
    default: {},
  },

  hasLevel: {
    type: Function,
    default: () => {},
  },

  paramCompanyLevel: {
    type: Object,
    default: {},
  },
  paramLocation: {
    type: Object,
    default: {},
  },
  errorLevel: {
    type: Boolean,
    default: false,
  },
  originData: {
    type: Object,
    default: {},
  },
});

const emit = defineEmits(["changeCompanyLevel"]);

const data = defineModel();

const changeName = (val, obj) => {
  if (data.value.company_level === props.levels.GOVERNORATE) {
    if (data.value.fk_governorate) {
      data.value.name_ar = "مكتب " + "محافظة " + (obj?.name_ar || obj?.name || "");
      data.value.name_en = " office " + "Governorate " + (obj?.name_en || "");
    } else {
      data.value.name_ar = "";
      data.value.name_en = "";
    }
  } else if (data.value.company_level === props.levels.DIRECTORATE) {
    if (data.value.fk_directorate) {
      data.value.name_ar = "مكتب " + "مديرية " + (obj?.name_ar || obj?.name_ar || "");
      data.value.name_en = " office " + "Directorate " + (obj?.name_en || "");
    } else {
      data.value.name_ar = "";
      data.value.name_en = "";
    }
  }
};
</script>
