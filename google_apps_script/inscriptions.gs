/**
 * CFI-TECH — Google Apps Script
 * Enregistrement automatique des inscriptions dans Google Sheets
 *
 * DÉPLOIEMENT :
 * 1. Ouvrir Google Sheets → Extensions → Apps Script
 * 2. Coller ce code, remplacer SPREADSHEET_ID
 * 3. Déployer → Nouvelle déploiement → Application Web
 *    - Exécuter en tant que : Moi
 *    - Accès : Tout le monde
 * 4. Copier l'URL de déploiement dans Django settings: GOOGLE_SCRIPT_URL
 */

const SPREADSHEET_ID = 'VOTRE_SPREADSHEET_ID_ICI';
const SHEET_NAME = 'Inscriptions CFI-TECH';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const sheet = getOrCreateSheet();

    // Ajouter la ligne
    sheet.appendRow([
      data.reference   || '',
      data.nom         || '',
      data.prenom      || '',
      data.telephone   || '',
      data.email       || '',
      data.formation   || '',
      data.niveau      || '',
      data.message     || '',
      data.date        || new Date().toLocaleString('fr-FR'),
      'En attente',          // Statut
      '',                    // Notes admin
    ]);

    // Mise en forme de la nouvelle ligne
    const lastRow = sheet.getLastRow();
    sheet.getRange(lastRow, 1, 1, 11).setBackground('#EBF5FB');

    // Envoyer notification email admin
    sendAdminNotification(data);

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'success', message: 'Inscription enregistrée' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function getOrCreateSheet() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  let sheet = ss.getSheetByName(SHEET_NAME);

  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    // En-têtes
    const headers = [
      'Référence', 'Nom', 'Prénom', 'Téléphone', 'Email',
      'Formation', 'Niveau', 'Message', 'Date inscription', 'Statut', 'Notes'
    ];
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    sheet.getRange(1, 1, 1, headers.length)
      .setBackground('#1565C0')
      .setFontColor('#FFFFFF')
      .setFontWeight('bold')
      .setFontSize(11);
    sheet.setFrozenRows(1);
    sheet.setColumnWidth(1, 120);
    sheet.setColumnWidth(6, 250);
    sheet.setColumnWidth(8, 300);
  }
  return sheet;
}

function sendAdminNotification(data) {
  const adminEmail = 'cfitech3@gmail.com';
  const subject = `🔔 Nouvelle inscription CFI-TECH : ${data.prenom} ${data.nom}`;
  const body = `
Nouvelle inscription reçue !

📋 Référence  : ${data.reference}
👤 Candidat   : ${data.prenom} ${data.nom}
📞 Téléphone  : ${data.telephone}
📧 Email      : ${data.email || 'Non fourni'}
📚 Formation  : ${data.formation}
🎓 Niveau     : ${data.niveau}
💬 Message    : ${data.message || 'Aucun'}
📅 Date       : ${data.date}

---
Gérer les inscriptions : https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}
  `;
  MailApp.sendEmail({ to: adminEmail, subject: subject, body: body });
}

function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok', service: 'CFI-TECH Inscriptions API' }))
    .setMimeType(ContentService.MimeType.JSON);
}
