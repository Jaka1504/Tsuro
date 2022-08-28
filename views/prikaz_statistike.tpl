% vse = max(statistika["skupaj"] - statistika["prilagojene"] - statistika["nedokoncane"], 1)
% delez_zmag = 100 * statistika["zmage"] / vse
% delez_porazov = 100 * statistika["porazi"] / vse
% delez_izenacenj = 100 * statistika["izenacenja"] / vse
<div class="progress">
  <div class="progress-bar progress-bar-striped bg-success" role="progressbar" style="width: {{delez_zmag}}%" aria-valuenow="{{delez_zmag}}" aria-valuemin="0" aria-valuemax="100"></div>
  <div class="progress-bar progress-bar-striped bg-dark" role="progressbar" style="width: {{delez_izenacenj}}%" aria-valuenow="{{delez_izenacenj}}" aria-valuemin="0" aria-valuemax="100"></div>
  <div class="progress-bar progress-bar-striped bg-danger" role="progressbar" style="width: {{delez_porazov}}%" aria-valuenow="{{delez_porazov}}" aria-valuemin="0" aria-valuemax="100"></div>
</div>