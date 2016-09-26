/*
 * Copyright 1999-2004 The Apache Software Foundation.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#if !defined(XALAN_GenerateEvent_HEADER_GUARD)
#define XALAN_GenerateEvent_HEADER_GUARD 



// Base include file.  Must be first.
#include <XSLTDefinitions.hpp>



#include <XalanDOMString.hpp>



XALAN_DECLARE_XERCES_CLASS(AttributeList)



XALAN_CPP_NAMESPACE_BEGIN



typedef XERCES_CPP_NAMESPACE_QUALIFIER AttributeList	AttributeListType;



/** 
 * This is the class for events generated by the XSL processor
 * after it generates a new node in the result tree.  It responds
 * to, and so is modeled from, the SAX events that are sent to the
 * FormatterListener classes.
 * 
 * @see org.apache.xml.xpath4j.xml.FormatterListener
 */
class XALAN_XSLT_EXPORT GenerateEvent
{
public:

	enum EventType
	{
		/** 
		 * Event type generated when a document begins.
		 * 
		 */
		EVENTTYPE_STARTDOCUMENT = 1,
			
		/** 
		 * Event type generated when a document ends.
		 */
		EVENTTYPE_ENDDOCUMENT = 2,
		
		/** 
		 * Event type generated when an element begins (after the attributes have been processed but before the children have been added).
		 */
		EVENTTYPE_STARTELEMENT = 3,
		
		/** 
		 * Event type generated when an element ends, after it's children have been added.
		 */
		EVENTTYPE_ENDELEMENT = 4,
		
		/** 
		 * Event type generated for character data (CDATA and Ignorable Whitespace have their own events).
		 */
		EVENTTYPE_CHARACTERS = 5,
		
		/** 
		 * Event type generated for ignorable whitespace (I'm not sure how much this is actually called.
		 */
		EVENTTYPE_IGNORABLEWHITESPACE = 6,

		/** 
		 * Event type generated for processing instructions.
		 */
		EVENTTYPE_PI = 7,

		/** 
		 * Event type generated after a comment has been added.
		 */
		EVENTTYPE_COMMENT = 8,

		/** 
		 * Event type generate after an entity ref is created.
		 */
		EVENTTYPE_ENTITYREF = 9,

		/** 
		 * Event type generated after CDATA is generated.
		 */
		EVENTTYPE_CDATA = 10
	};


	/** 
	 * Constructor for startDocument, endDocument events.
	 * 
	 * @param eventType one of the EVENTTYPE_XXX constants
	 */
	GenerateEvent(EventType		eventType);
	
	/** 
	* Constructor for startElement, endElement events.
	* 
	* @param eventType one of the EVENTTYPE_XXX constants
	* @param name      name of the element
	* @param atts      SAX attribute list
	*/
	GenerateEvent(
			EventType				eventType,
			const XalanDOMChar*		name,
			AttributeListType*		atts);

	/** 
	* Constructor for startElement, endElement events.
	* 
	* @param eventType one of the EVENTTYPE_XXX constants
	* @param name      name of the element
	* @param atts      SAX attribute list
	*/
	GenerateEvent(
			EventType					eventType,
			const XalanDOMString&		name,
			const AttributeListType*	atts = 0);

	/** 
	* Constructor for characters, cdate events.
	*
	* @param eventType one of the EVENTTYPE_XXX constants
	* @param ch        char array from the SAX event
	* @param start     start offset to be used in the char array
	* @param length    end offset to be used in the chara array
	*/
	GenerateEvent(
			EventType					eventType,
			const XalanDOMChar*			ch,
			XalanDOMString::size_type	start,
			XalanDOMString::size_type	length);
	
	/** 
	* Constructor for processingInstruction events.
	* 
	* @param eventType one of the EVENTTYPE_XXX constants
	* @param name      name of the processing instruction
	* @param data      processing instruction data
	*/
	GenerateEvent(
			EventType				eventType,
			const XalanDOMChar*		name,
			const XalanDOMChar*		data);
	
	/** 
	* Constructor for comment and entity ref events.
	* 
	* @param processor XSLT processor instance
	* @param eventType one of the EVENTTYPE_XXX constants
	* @param data      comment or entity ref data
	*/
	GenerateEvent(
			EventType				eventType,
			const XalanDOMChar*		data);

	/** 
	 * The type of SAX event that was generated, as enumerated in the
	 * EVENTTYPE_XXX constants above.
	 */
	EventType				m_eventType;

	/** 
	 * Character data from a character or cdata event.
	 */
	XalanDOMString			m_characters;

	/** 
	 * The start position of the current data in m_characters.
	 */
	XalanDOMString::size_type	m_start;

	/** 
	 * The length of the current data in m_characters.
	 */
	XalanDOMString::size_type	m_length;

	/** 
	 * The name of the element or PI.
	 */
	XalanDOMString			m_name;

	/** 
	 * The string data in the element (comments and PIs).
	 */
	XalanDOMString			m_data;

	/** 
	 * The current attribute list.
	 */
	const AttributeListType*	m_pAtts;
};



XALAN_CPP_NAMESPACE_END



#endif	//XALAN_GenerateEvent_HEADER_GUARD
