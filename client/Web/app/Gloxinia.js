class Central {
    constructor () {
        this.central = document.getElementById('central')
        this.appendElement = function (element) { this.central.appendChild(element) }
        this.removeElement = function (element) { this.central.removeChild(element) }
    }
}

class Button {
    constructor () {
        this.button = document.createElement('button')
        this.button.innerText = 'Button'
        this.button.classList.add('Button')
        this.button.setAttribute('onpointerdown', 'ripplet(arguments[0], {color:\'white\', opacity:\'0.2\', spreadingDuration:\'0.2s\'})')
        this.setButtonSize = function (width, height) { this.button.width = width; this.button.height = height }
        this.setButtonText = function (text) { this.button.innerText = text; this.loadIcon() }
        this.setButtonTextColor = function (color) { this.button.style.color = color }
        this.addButtonClass = function (clss) { this.button.classList.add(clss) }
        this.setButtonColor = function (color) { this.button.style.backgroundColor = color }

        this.icon = document.createElement('img')
        this.icon.src = ''
        this.icon.classList.add('Button-Icon')
        this.loadIcon = function () { if (this.icon.src != document.URL) { this.button.prepend(this.icon) } else { if (Array.from(this.button.childNodes).includes(this.icon)) { this.button.removeChild(this.icon) } } }
        this.setIconSrc = function (src) { this.icon.src = src; this.loadIcon() }
        this.addIconClass = function (clss) { this.icon.classList.add(clss) }
        this.setIconSize = function (width, height) { this.icon.style.width = width; this.icon.style.height = height}
        this.setIconTop = function (boolean) { if (boolean == true) { this.button.style.flexDirection = 'column'} else { this.button.style.flexDirection = 'row' } }
        
        this.element = function () { return this.button }
    }
}

class TextField {
    constructor () {
        this.textfield = document.createElement('div')
        this.textfield.classList.add('TextField')

        this.inputfield = document.createElement('div')
        this.inputfield.classList.add('TextField-Inputfield')

        this.fieldIcons = document.createElement('div')
        this.fieldIcons.classList.add('TextField-Icons')
        this.fieldTexts = document.createElement('div')
        this.fieldTexts.classList.add('TextField-Texts')

        this.fieldhint = document.createElement('label')
        this.fieldhint.classList.add('TextField-FieldHint')
        this.fieldhint.innerText = 'PLACEHOLDER'
        this.fieldIcons.appendChild(this.fieldhint)

        this.leadicon = document.createElement('img')
        this.leadicon.src = ''
        this.leadicon.classList.add('TextField-LeadIcon')
        this.loadLeadIcon = function () { if (this.leadicon.src != document.URL) { this.fieldIcons.prepend(this.leadicon); this.inputbox.style.paddingLeft = '2rem' } else { this.fieldIcons.removeChild(this.leadicon); this.inputbox.style.paddingLeft = '0.7rem' }}
        
        this.setLeadIconSrc = function (src) { this.leadicon.src = src; this.loadLeadIcon() }
        this.inputbox = document.createElement('input')
        this.inputbox.classList.add('TextField-InputBox')
        // this.inputfield.setAttribute('onkeyup', 'reloadCharaCounter(this.id)')
        this.inputbox.required = true

        this.trailingicon = document.createElement('button')

        this.assistivetext = document.createElement('label')
        this.assistivetext.classList.add('TextField-AssistiveText')
        this.assistivetext.innerText = 'Assistive Text'
        this.fieldTexts.appendChild(this.assistivetext)
        
        this.characounter = document.createElement('label')
        this.characounter.classList.add('TextField-CharaCounter')
        this.characounter.innerText = '0 / 10'
        this.fieldTexts.appendChild(this.characounter)

        this.inputfield.appendChild(this.inputbox)
        this.inputfield.appendChild(this.fieldIcons)

        this.textfield.appendChild(this.inputfield)
        this.textfield.appendChild(this.fieldTexts)
    }
}

function textfield_charcounter() {

}

class ListItem {
    constructor () {
        this.item = document.createElement('div')
        this.item.classList.add('ListItem')

        this.thumbnail = document.createElement('img')
        this.thumbnail.classList.add('ListItem-Thumbnail')
        this.thumbnail.src = './assets/button/lock.svg'

        this.lines = document.createElement('div')
        this.lines.classList.add('ListItem-Lines')

        this.lineTop = document.createElement('div')
        this.lineTop.classList.add('ListItem-LineTop')

        this.lineMiddle = document.createElement('div')
        this.lineMiddle.classList.add('ListItem-LineMiddle')

        this.lineBottom = document.createElement('div')
        this.lineBottom.classList.add('ListItem-LineBottom')

        this.title = document.createElement('a')
        this.title.classList.add('ListItem-Title')
        this.title.innerText = 'Title'
        
        this.details = document.createElement('button')

        this.buttontest = new Button()
        this.buttontest.element().classList.add('ListItem-ButtonTest')
        this.buttontest.setButtonColor('red')
        this.buttontest.setButtonText('')
        this.buttontest.setIconSrc('./assets/button/lock.svg')

        this.buttontest2 = new Button()
        this.buttontest3 = new Button()
        
        this.edit = document.createElement('button')

        this.tagviewer = document.createElement('div')

        this.tagedit = document.createElement('button')

        this.resolution = document.createElement('a')

        this.format = document.createElement('a')

        this.lineTop.appendChild(this.title)
        this.lineTop.appendChild(this.buttontest.element())

        this.lineMiddle.appendChild(this.buttontest2.element())
        this.lineBottom.appendChild(this.buttontest3.element())

        this.lines.appendChild(this.lineTop)
        this.lines.appendChild(this.lineMiddle)
        this.lines.appendChild(this.lineBottom)

        this.item.appendChild(this.thumbnail)
        this.item.appendChild(this.lines)
        
    }
}

let view = new Central()

let inline = document.createElement('div')
inline.style.display = 'flex'

let mtbtn = new Button()
mtbtn.setButtonText('연티와 멍티의 버튼')
mtbtn.setButtonColor('orange')
mtbtn.setIconSrc('./assets/button/lock.svg')
mtbtn.setButtonTextColor('black')
mtbtn.setIconTop(true)

let tb = new TextField()

inline.appendChild(tb.textfield)
inline.appendChild(mtbtn.element())

view.appendElement(inline)

// view.appendElement(mtbtn.element())
// view.appendElement(tb.textfield)