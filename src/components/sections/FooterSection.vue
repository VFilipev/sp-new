<script setup>
import nationalProjectsLogo from "@/assets/resort/national-projects-logo.png";
const currentYear = new Date().getFullYear();
</script>

<template>
  <footer id="contacts" class="bg-muted py-12 md:py-16">
    <div class="container mx-auto px-4">
      <div class="mb-12 grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-5">
        <div>
          <h4 class="mb-4 font-semibold text-foreground">
            размещение и проживание
          </h4>
          <ul class="space-y-2 text-sm text-muted-foreground">
            <li>
              <a
                href="#lodge"
                class="transition-colors hover:text-foreground"
                >дома</a
              >
            </li>
            <li>
              <a href="#active" class="transition-colors hover:text-foreground"
                >активный отдых и услуги</a
              >
            </li>
            <li>
              <a href="#" class="transition-colors hover:text-foreground"
                >главная страница</a
              >
            </li>
          </ul>
        </div>

        <div>
          <h4 class="mb-4 font-semibold text-foreground">контакты</h4>
          <ul class="space-y-2 text-sm text-muted-foreground">
            <li>
              <a
                href="tel:+79026439294"
                class="transition-colors hover:text-foreground"
                >+7 (902) 643-92-94</a
              >
            </li>
            <li>
              <a
                href="tel:+73422880089"
                class="transition-colors hover:text-foreground"
                >+7 (342) 288-00-89</a
              >
            </li>
            <li>
              <a
                href="mailto:stroganovprostor@gmail.com"
                class="transition-colors hover:text-foreground"
                >stroganovprostor@gmail.com</a
              >
            </li>
          </ul>
        </div>

        <div>
          <h4 class="mb-4 font-semibold text-foreground">адрес</h4>
          <p class="text-sm leading-relaxed text-muted-foreground">
            Пермский край, Ильинский<br />
            район, п. Ильинский,<br />
            с. Дмитриевское
          </p>
        </div>

        <div>
          <h4 class="mb-4 font-semibold text-foreground">правовые документы</h4>
          <ul class="space-y-2 text-sm text-muted-foreground">
            <li>
              <a href="#" class="transition-colors hover:text-foreground"
                >Согласие на обработку<br />персональных данных</a
              >
            </li>
            <li>
              <a href="#" class="transition-colors hover:text-foreground"
                >Политика конфиденциальности</a
              >
            </li>
          </ul>
        </div>

        <div>
          <h4 class="mb-4 font-semibold text-foreground">мы в соцсетях</h4>
          <div class="flex gap-3">
            <a
              href="https://t.me/"
              target="_blank"
              rel="noopener noreferrer"
              class="flex h-10 w-10 items-center justify-center rounded-full bg-muted-foreground/20 transition-colors hover:bg-primary hover:text-primary-foreground"
            >
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"
                />
              </svg>
            </a>
            <a
              href="https://vk.com/"
              target="_blank"
              rel="noopener noreferrer"
              class="flex h-10 w-10 items-center justify-center rounded-full bg-muted-foreground/20 transition-colors hover:bg-primary hover:text-primary-foreground"
            >
              <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                <path
                  d="M15.684 0H8.316C1.592 0 0 1.592 0 8.316v7.368C0 22.408 1.592 24 8.316 24h7.368C22.408 24 24 22.408 24 15.684V8.316C24 1.592 22.408 0 15.684 0zm3.692 17.123h-1.744c-.66 0-.864-.525-2.05-1.727-1.033-1-1.49-1.135-1.744-1.135-.356 0-.458.102-.458.593v1.575c0 .424-.135.678-1.253.678-1.846 0-3.896-1.118-5.335-3.202C4.624 10.857 4 8.624 4 8.12c0-.254.102-.491.593-.491h1.744c.44 0 .61.203.78.678.847 2.473 2.27 4.64 2.862 4.64.22 0 .322-.102.322-.66V9.721c-.068-1.186-.695-1.287-.695-1.71 0-.203.17-.407.44-.407h2.744c.373 0 .508.203.508.644v3.473c0 .372.17.508.271.508.22 0 .407-.136.813-.542 1.254-1.406 2.15-3.574 2.15-3.574.119-.254.322-.491.763-.491h1.744c.525 0 .644.27.525.644-.22 1.017-2.354 4.031-2.354 4.031-.186.305-.254.44 0 .78.186.254.796.779 1.203 1.253.745.847 1.32 1.558 1.473 2.05.17.49-.085.744-.576.744z"
                />
              </svg>
            </a>
          </div>
        </div>
      </div>

      <div class="mb-8 border-t border-border pt-8">
        <div
          class="flex flex-col items-center justify-center gap-4 text-center md:flex-row"
        >
          <img
            :src="nationalProjectsLogo"
            alt="Национальные проекты России"
            class="h-32 w-auto"
          />
          <div class="text-sm text-muted-foreground">
            <p>
              Единый реестр объектов классификации в сфере туристской индустрии
            </p>
            <p class="font-medium">Номер реестровой записи:</p>
            <a
              href="https://tourism.fsa.gov.ru/ru/resorts/hotels/d25e4a6c-c607-11ef-92da-e7d07e8e684c/about-resort"
              >С592024018790</a
            >
          </div>
        </div>
      </div>

      <div
        class="flex flex-col items-center justify-between gap-4 border-t border-border pt-6 md:flex-row"
      >
        <p class="text-sm text-muted-foreground">
          © СТРОГАНОВСКИЕ ПРОСТОРЫ 2017—{{ currentYear }}
        </p>
        <p class="text-sm text-muted-foreground">Пермь. Официальный сайт.</p>
      </div>
    </div>
  </footer>
</template>
