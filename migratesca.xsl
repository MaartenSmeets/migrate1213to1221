<xsl:stylesheet
    version="1.0"
    xmlns:src="http://maven.apache.org/POM/4.0.0" 
    xmlns="http://maven.apache.org/POM/4.0.0"   
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:namespace-alias stylesheet-prefix="src" result-prefix=""/>

	<xsl:template match="/src:project/src:parent/src:version">
		<src:version>12.2.1-0-0</src:version>
	</xsl:template>

	<xsl:template match="/src:project/src:build/src:plugins/src:plugin/src:version">
		<src:version>12.2.1-0-0</src:version>
	</xsl:template>

	<xsl:template match="@*|node()">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()"/>
		</xsl:copy>
	</xsl:template>
</xsl:stylesheet>