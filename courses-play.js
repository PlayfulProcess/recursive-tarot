// Courses live in recursive.eco since Oct 23 2026: each one is a grammar in tarot/<id>-course/
// (tarot/how-to-contribute for that one), read in Play's Continuous view. This is the one map from
// a course id to its recursive.eco grammar (the ids come from tarot/_eco_ids.json). site-header.js,
// pages/courses.html, quick-jump.js and the old address pages/course-viewer.html read it.
// A course that is still Private in recursive.eco is left out, so its links fall back to the
// course list. Publishing one? Add its line here.
window.COURSE_PLAY = {
  "divination-traditions": "420b5ef6-da19-4eb6-aae3-6e0e2ba53113",
  "games-of-the-tarot": "e9e0aa7d-48a0-467b-911d-5096d8c745ff",
  "golden-dawn-dignities-not-reversals": "f630cfc4-6b65-4f42-9316-7bea4016e29b",
  "golden-dawn-where-the-cards-went": "c5d8231e-3e1e-4985-a6a5-f974e670570a",
  "history-of-tarot": "4f954864-6889-4bf7-8b2e-64e313066444",
  "hospicing-modernity-reads-the-tarot": "5104a4cc-4c9d-46dc-a415-2687e95ba9bf",
  "how-tarot-works": "f824e706-af68-4cf9-98ad-2977b69e1e4e",
  "intention-setting": "f08856eb-7fa6-40d4-818a-ee5f520fb30b",
  "jung-reads-the-tarot": "17acdf81-384d-455a-b573-e82ea42926b7",
  "kant-and-the-tarot": "f3ae903c-bbce-4dcd-b773-746edf7c09cd",
  "marsha-linehan-reads-the-tarot": "ba765c72-7f75-40c0-8b80-f37d8fa7fad6",
  "morality-is-an-ecosystem": "13eb2ca4-f001-4dcf-8763-4ee1b16efd00",
  "non-dual-tantra-reads-the-tarot": "2b309dfb-928c-4985-b1ec-5d0346c07512",
  "post-activism-reads-the-tarot": "c6d916ca-8cc1-430b-86b4-0e15c7e5dc15",
  "reading-the-cards": "c61b042b-0a0a-4537-99ad-eef2c2852ca5",
  "same-card-every-deck": "d6ac6fe1-4580-4cde-bc49-1d1cd3352df3",
  "tarot-and-fiction": "e37ff310-da25-4d7e-9dbb-ce26b6b514d6",
  "tarot-and-the-crack": "d2852625-7fb8-4583-96c7-041753703e4f",
  "the-order-of-the-trumps": "767ed56e-19bd-41e8-b994-46ca7022a896",
  "walking-the-golden-dawn-path": "9befd48e-5c83-48aa-abb2-d865beb06c19",
  "what-a-reading-can-do": "6f7b419b-e740-45b1-ba82-728dc79b0317",
  "why-a-reading-feels-personal": "2db347d9-00ca-483f-bd09-10f762efe859",
  "working-with-claude-desktop": "afc14912-a8d1-4040-b451-022841784a55",
  "how-to-contribute": "368974ce-0718-4e9a-9351-bce7b2c053e4"
};
window.coursePlayUrl = function (id, node) {
  var g = window.COURSE_PLAY[id];
  if (!g) return null;
  return 'https://recursive.eco/play?id=' + g + '&pane=continuous' + (node ? '&node=' + encodeURIComponent(node) : '');
};
